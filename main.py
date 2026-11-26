from datetime import datetime
import json
import os
import queue
import re
import time
from dotenv import load_dotenv
import numpy as np
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusTcpClient
from definitions import (
    ALARM_CODES,
    ALARM_TYPES,
    FAULT_CODES,
    FAULT_TYPES,
    controls,
    derived_sensors,
    device_info,
    sensor_details,
    sensors,
)

load_dotenv()

TIME_HM_PATTERN = r"^([01][0-9]|2[0-3]):[0-5][0-9]$"


def is_writes_enabled():
    return os.getenv("ENABLE_MODBUS_WRITES", "false").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )

## Convert received Modbus data

def convert_to_signed_32bit(high, low):
    value = (high << 16) | low
    if value >= 0x80000000:
        value -= 0x100000000
    return value

def convert_to_unsigned_32bit(high, low):
    return np.uint32((high << 16) | low)

def convert_to_unsigned_16bit(value):
    return np.uint16(value)

def convert_to_signed_16bit(value):
    if value >= 0x8000:
        value -= 0x10000
    return value

## Read specific Modbus address, convert the received data depending on the specified type, scale it, round it and return it.

def _decimals_for_scale(scale):
    if isinstance(scale, int):
        return 0
    formatted = f"{scale:.10f}".rstrip("0")
    if "." in formatted:
        return len(formatted.split(".")[1])
    return 0


def read_sensor_value(client, address, slave, data_type, scale=1, value_map=None):
    if data_type in ["U16", "S16"]:
        rr = client.read_holding_registers(address=address, count=1, slave=slave)
    elif data_type in ["S32", "U32"]:
        rr = client.read_holding_registers(address=address, count=2, slave=slave)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

    if rr.isError():
        raise Exception(f"Error reading registers at address {address}")

    if data_type == "U16":
        raw_value = int(convert_to_unsigned_16bit(rr.registers[0]))
    elif data_type == "S16":
        raw_value = int(convert_to_signed_16bit(rr.registers[0]))
    elif data_type == "S32":
        high, low = rr.registers
        raw_value = int(convert_to_signed_32bit(high, low))
    elif data_type == "U32":
        high, low = rr.registers
        raw_value = int(convert_to_unsigned_32bit(high, low))

    if value_map is not None:
        return value_map.get(raw_value, f"Unknown ({raw_value})")

    decimals = _decimals_for_scale(scale)
    if decimals == 0:
        return int(raw_value * scale)
    return round(float(raw_value) * scale, decimals)


def read_serial_number(client, slave=1):
    rr = client.read_holding_registers(address=0x3001, count=16, slave=slave)
    if rr.isError():
        raise Exception("Error reading serial number registers at address 0x3001")
    raw_bytes = bytearray()
    for reg in rr.registers:
        for byte in ((reg >> 8) & 0xFF, reg & 0xFF):
            if byte not in (0x00, 0xFF):
                raw_bytes.append(byte)
    return raw_bytes.decode("ascii", errors="ignore").strip()


def read_sw_version(client, slave=1):
    rr = client.read_holding_registers(address=0x3802, count=4, slave=slave)
    if rr.isError():
        raise Exception("Error reading software version registers at address 0x3802")
    return "-".join(str(int(convert_to_unsigned_16bit(r))) for r in rr.registers)


def populate_device_info(client, base_device_info, slave=1):
    info = dict(base_device_info)

    try:
        serial_number = read_serial_number(client, slave=slave)
        if serial_number:
            info["serial_number"] = serial_number
    except Exception as e:
        print(f"Error reading serial number: {e}")

    if "serial_number" not in info:
        fallback_serial = os.getenv("INVT_SERIAL_NUMBER")
        if fallback_serial:
            info["serial_number"] = fallback_serial

    try:
        sw_version = read_sw_version(client, slave=slave)
        if sw_version:
            info["sw_version"] = sw_version
    except Exception as e:
        print(f"Error reading software version: {e}")

    return info

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_status_code(main_code, sub_code, code_map, type_map, none_label):
    if main_code is None or sub_code is None:
        return None
    if main_code == 0 and sub_code == 0:
        return none_label
    code_str = f"{main_code:02d}-{sub_code:02d}"
    description = code_map.get((main_code, sub_code))
    if description:
        return f"{code_str}: {description}"
    category = type_map.get(main_code)
    if category:
        return f"{code_str}: {category}"
    return f"{code_str}: Unknown"


## Auto discovery for Home Assistant

def publish_discovery_messages(client, sensors, device_info):
    all_sensor_configs = {**sensors, **{sid: {} for sid in derived_sensors}}
    for sensor_id, config in all_sensor_configs.items():
        details = sensor_details.get(sensor_id, {})
        discovery_payload = {
            "name": details.get("name", sensor_id),
            "state_topic": os.getenv("MQTT_TOPIC"),
            "value_template": "{{ value_json." + sensor_id + " }}",
            "unique_id": f"modbus_{sensor_id}",
            "device": device_info,
        }
        if details.get("device_class"):
            discovery_payload["device_class"] = details["device_class"]
        if details.get("state_class"):
            discovery_payload["state_class"] = details["state_class"]
        if config.get("unit"):
            discovery_payload["unit_of_measurement"] = config["unit"]
        if details.get("icon"):
            discovery_payload["icon"] = details["icon"]

        discovery_topic = f"homeassistant/sensor/{sensor_id}/config"
        client.publish(discovery_topic, json.dumps(discovery_payload), retain=True)


def decode_control_value(raw_value, config):
    component = config["component"]
    if component == "select":
        return config["options"].get(raw_value)
    if component == "switch":
        if raw_value == 1:
            return "ON"
        if raw_value == 0:
            return "OFF"
        return None
    if component == "number":
        return int(raw_value)
    if component == "text" and config.get("value_type") == "hm":
        hour = (raw_value >> 8) & 0xFF
        minute = raw_value & 0xFF
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
        return None
    return None


def encode_control_value(payload, config):
    component = config["component"]
    text = payload.strip()

    if component == "select":
        for code, label in config["options"].items():
            if text == label:
                return code
        raise ValueError(f"Invalid option '{payload}' for {config['name']}")

    if component == "switch":
        upper = text.upper()
        if upper == "ON":
            return 1
        if upper == "OFF":
            return 0
        raise ValueError(f"Invalid switch payload '{payload}' for {config['name']}")

    if component == "number":
        try:
            numeric = float(text)
        except ValueError as err:
            raise ValueError(f"Invalid numeric payload '{payload}' for {config['name']}") from err
        if not numeric.is_integer():
            raise ValueError(f"Expected integer value, got '{payload}' for {config['name']}")
        val = int(numeric)
        if val < config["min"] or val > config["max"]:
            raise ValueError(
                f"Value {val} out of range [{config['min']}, {config['max']}] for {config['name']}"
            )
        return val

    if component == "text" and config.get("value_type") == "hm":
        if not re.match(TIME_HM_PATTERN, text):
            raise ValueError(f"Invalid HH:MM time '{payload}' for {config['name']}")
        hour, minute = (int(part) for part in text.split(":"))
        return (hour << 8) | minute

    raise ValueError(f"Unsupported control component: {component}")


def _read_control_block(client, start_addr, count, slave):
    rr = client.read_holding_registers(address=start_addr, count=count, slave=slave)
    if rr.isError() or len(rr.registers) != count:
        raise Exception(f"Error reading control block 0x{start_addr:04X} (count={count})")
    return {
        start_addr + i: int(convert_to_unsigned_16bit(reg))
        for i, reg in enumerate(rr.registers)
    }


def read_control_states(client, slave=1):
    addr_values = {}
    read_ranges = (
        (0x3118, 31),
        (0x3160, 2),
        (0x3111, 1),
        (0x313C, 1),
    )

    for start_addr, count in read_ranges:
        try:
            addr_values.update(_read_control_block(client, start_addr, count, slave))
        except Exception:
            end_addr = start_addr + count - 1
            for control_id, config in controls.items():
                if config["component"] == "button":
                    continue
                addr = config["address"]
                if start_addr <= addr <= end_addr:
                    try:
                        addr_values.update(_read_control_block(client, addr, 1, slave))
                    except Exception as err:
                        print(f"Error reading control {control_id}: {err}")

    states = {}
    raw_values = {}
    for control_id, config in controls.items():
        if config["component"] == "button":
            continue
        raw_val = addr_values.get(config["address"])
        if raw_val is None:
            continue
        decoded = decode_control_value(raw_val, config)
        if decoded is not None:
            states[control_id] = decoded
            raw_values[control_id] = raw_val

    return states, raw_values


def handle_control_command(client, control_id, payload, last_raw_values, slave=1):
    if not is_writes_enabled() or control_id not in controls:
        return False

    config = controls[control_id]

    if config.get("action") == "sync_clock":
        if payload.strip().upper() != "PRESS":
            raise ValueError(f"Invalid button payload '{payload}' for {control_id}")
        now = datetime.now()
        year_2d = now.year % 100
        if not (20 <= year_2d <= 99):
            raise ValueError(f"System year {now.year} out of inverter RTC range (2020-2099)")
        values = [
            (year_2d << 8) | now.month,
            (now.day << 8) | now.hour,
            (now.minute << 8) | now.second,
        ]
        rr = client.write_registers(address=0x3014, values=values, slave=slave)
        if rr.isError():
            raise Exception("Error writing clock registers at address 0x3014")
        print(f"Synced inverter clock to {now.strftime('%Y-%m-%d %H:%M:%S')}")
        return True

    raw_val = encode_control_value(payload, config)
    if last_raw_values.get(control_id) == raw_val:
        print(f"Skipping write for {control_id}: value unchanged ({payload.strip()})")
        return True

    rr = client.write_registers(address=config["address"], values=[raw_val], slave=slave)
    if rr.isError():
        raise Exception(
            f"Error writing register 0x{config['address']:04X} for {control_id}"
        )
    print(f"Wrote {control_id} (0x{config['address']:04X}) = {raw_val} ({payload.strip()})")
    return True


def publish_control_discovery_messages(mqtt_client, device_info):
    base_topic = os.getenv("MQTT_TOPIC")
    state_topic = f"{base_topic}/controls"

    for control_id, config in controls.items():
        component = config["component"]
        discovery_payload = {
            "name": config["name"],
            "unique_id": f"modbus_ctrl_{control_id}",
            "device": device_info,
            "command_topic": f"{base_topic}/set/{control_id}",
            "entity_category": "config",
        }
        if config.get("icon"):
            discovery_payload["icon"] = config["icon"]

        if component != "button":
            discovery_payload["state_topic"] = state_topic
            discovery_payload["value_template"] = "{{ value_json." + control_id + " }}"

        if component == "select":
            discovery_payload["options"] = list(config["options"].values())
        elif component == "switch":
            discovery_payload["payload_on"] = "ON"
            discovery_payload["payload_off"] = "OFF"
            discovery_payload["state_on"] = "ON"
            discovery_payload["state_off"] = "OFF"
        elif component == "number":
            discovery_payload["min"] = config["min"]
            discovery_payload["max"] = config["max"]
            discovery_payload["step"] = config["step"]
            discovery_payload["unit_of_measurement"] = config["unit"]
            discovery_payload["mode"] = "box"
        elif component == "text":
            discovery_payload["pattern"] = TIME_HM_PATTERN
            discovery_payload["min"] = 5
            discovery_payload["max"] = 5
            discovery_payload["mode"] = "text"
        elif component == "button":
            discovery_payload["payload_press"] = "PRESS"

        discovery_topic = f"homeassistant/{component}/{control_id}/config"
        mqtt_client.publish(discovery_topic, json.dumps(discovery_payload), retain=True)


def main():
    mqtt_topic = os.getenv("MQTT_TOPIC")
    writes_enabled = is_writes_enabled()
    update_interval = int(os.getenv("UPDATE_INTERVAL"))
    command_queue = queue.Queue()

    print("Modbus writes: ENABLED" if writes_enabled else "Modbus writes: DISABLED (read-only mode)")

    def handle_connect(client_obj, userdata, flags, rc):
        on_connect(client_obj, userdata, flags, rc)
        if writes_enabled:
            client_obj.subscribe(f"{mqtt_topic}/set/+")

    def handle_message(client_obj, userdata, msg):
        if not writes_enabled:
            return
        prefix = f"{mqtt_topic}/set/"
        if not msg.topic.startswith(prefix):
            return
        control_id = msg.topic[len(prefix):]
        payload = msg.payload.decode("utf-8", errors="ignore")
        command_queue.put((control_id, payload))

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    mqtt_client.on_connect = handle_connect
    if writes_enabled:
        mqtt_client.on_message = handle_message
    mqtt_client.connect(os.getenv("MQTT_BROKER_ADDRESS"), 1883, 60)
    mqtt_client.loop_start()

    client = ModbusTcpClient(os.getenv("MODBUS_TCP_IP"))
    client.connect()

    try:

        resolved_device_info = populate_device_info(client, device_info, slave=1)
        publish_discovery_messages(mqtt_client, sensors, resolved_device_info)
        if writes_enabled:
            publish_control_discovery_messages(mqtt_client, resolved_device_info)

        last_raw_values = {}

        while True:
            results = {}

            for sensor, config in sensors.items():
                try:
                    value = read_sensor_value(
                        client,
                        config["address"],
                        slave=1,
                        data_type=config["type"],
                        scale=config["scale"],
                        value_map=config.get("value_map")
                    )
                    results[sensor] = value
                except Exception as e:
                    results[sensor] = None
                    print(f"Error reading {sensor}: {e}")

            results["FAULT_STATUS"] = format_status_code(
                results.get("MAIN_FAULT_CODE"),
                results.get("SUB_FAULT_CODE"),
                FAULT_CODES,
                FAULT_TYPES,
                "No Fault",
            )
            results["ALARM_STATUS"] = format_status_code(
                results.get("MAIN_ALARM_CODE"),
                results.get("SUB_ALARM_CODE"),
                ALARM_CODES,
                ALARM_TYPES,
                "No Alarm",
            )

            json_payload = json.dumps(results)
            mqtt_client.publish(mqtt_topic, json_payload)

            if writes_enabled:
                control_states, last_raw_values = read_control_states(client, slave=1)
                mqtt_client.publish(
                    f"{mqtt_topic}/controls",
                    json.dumps(control_states),
                    retain=True,
                )

            clear_console()

            #pprint.pprint(results)
            for key, value in results.items():
                print(f"{key}: {value}")

            if writes_enabled:
                deadline = time.monotonic() + update_interval
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    try:
                        control_id, payload = command_queue.get(timeout=remaining)
                    except queue.Empty:
                        break
                    try:
                        if handle_control_command(
                            client, control_id, payload, last_raw_values, slave=1
                        ):
                            control_states, last_raw_values = read_control_states(
                                client, slave=1
                            )
                            mqtt_client.publish(
                                f"{mqtt_topic}/controls",
                                json.dumps(control_states),
                                retain=True,
                            )
                    except Exception as e:
                        print(f"Error handling control command {control_id}: {e}")
            else:
                time.sleep(update_interval)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        client.close()

if __name__ == "__main__":
    main()