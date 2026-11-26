import time
import json
from pymodbus.client import ModbusTcpClient
import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
from definitions import sensors, sensor_details, device_info

load_dotenv()

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

## Auto discovery for Home Assistant

def publish_discovery_messages(client, sensors, device_info):
    
    for sensor_id, config in sensors.items():
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

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(os.getenv("MQTT_BROKER_ADDRESS"), 1883, 60)

    client = ModbusTcpClient(os.getenv("MODBUS_TCP_IP"))
    client.connect()

    try:

        resolved_device_info = populate_device_info(client, device_info, slave=1)
        publish_discovery_messages(mqtt_client, sensors, resolved_device_info)

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

            json_payload = json.dumps(results)
            mqtt_client.publish(os.getenv("MQTT_TOPIC"), json_payload)

            clear_console()

            #pprint.pprint(results)
            for key, value in results.items():
                print(f"{key}: {value}")
            mqtt_client.loop(2)
            time.sleep(int(os.getenv("UPDATE_INTERVAL")))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()