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

def read_sensor_value(client, address, slave, data_type, scale=1.0):
    if data_type in ["U16", "S16"]:
        rr = client.read_holding_registers(address=address, count=1, slave=slave)
    elif data_type in ["S32", "U32"]:
        rr = client.read_holding_registers(address=address, count=2, slave=slave)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

    if rr.isError():
        raise Exception(f"Error reading registers at address {address}")

    if data_type == "U16":
        return round(float(convert_to_unsigned_16bit(rr.registers[0])) * scale, 1)
    elif data_type == "S16":
        return round(float(convert_to_signed_16bit(rr.registers[0])) * scale, 1)
    elif data_type == "S32":
        high, low = rr.registers
        return round(float(convert_to_signed_32bit(high, low)) * scale, 1)
    elif data_type == "U32":
        high, low = rr.registers
        return round(float(convert_to_unsigned_32bit(high, low)) * scale, 1)

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
            "device_class": details.get("device_class"),
            "state_class": details.get("state_class"),
            "unit_of_measurement": config["unit"],
            "value_template": "{{ value_json." + sensor_id + " }}",
            "unique_id": f"modbus_{sensor_id}",
            "device": device_info,
            "icon": details.get("icon")
        }
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

        publish_discovery_messages(mqtt_client, sensors, device_info)

        while True:
            results = {}

            for sensor, config in sensors.items():
                try:
                    value = read_sensor_value(
                        client,
                        config["address"],
                        slave=1,
                        data_type=config["type"],
                        scale=config["scale"]
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