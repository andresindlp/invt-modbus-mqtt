import time
import json
from pymodbus.client import ModbusTcpClient
import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os


load_dotenv()

def convert_to_signed_32bit(high, low):
    """Combine two 16-bit registers into a signed 32-bit integer."""
    value = (high << 16) | low
    if value >= 0x80000000:
        value -= 0x100000000
    return value

def convert_to_unsigned_32bit(high, low):
    value = (high << 16) | low
    return np.uint32(value)

def convert_to_unsigned_16bit(value):
    return np.uint16(value)

def convert_to_signed_16bit(value):
    """Convert a 16-bit register to a signed 16-bit integer."""
    if value >= 0x8000:
        value -= 0x10000
    return value

def read_sensor_value(client, address, slave, data_type, scale=1.0):
    if data_type in ["U16", "S16"]:
        rr = client.read_holding_registers(address=address, count=1, slave=slave)
    elif data_type in ["S32", "U32"]:
        rr = client.read_holding_registers(address=address, count=2, slave=slave)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

    if rr.isError():
        raise Exception(f"Error reading registers at address {address}: {rr}")

    if data_type == "U16":
        return convert_to_unsigned_16bit(rr.registers[0]) * scale
    elif data_type == "S16":
        return convert_to_signed_16bit(rr.registers[0]) * scale
    elif data_type == "S32":
        high, low = rr.registers
        return convert_to_signed_32bit(high, low) * scale
    elif data_type == "U32":
        high, low = rr.registers
        return convert_to_unsigned_32bit(high, low) * scale


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(os.getenv("MQTT_BROKER_ADDRESS"), 1883, 60)

    client = ModbusTcpClient(os.getenv("MODBUS_TCP_IP"))
    client.connect()

    try:
        sensors = {
            "EPS_V": {"address": 0x3115, "type": "U16", "scale": 0.1},
            "PBUS_V": {"address": 0x380F, "type": "U16", "scale": 0.1},
            "GRID_V": {"address": 0x3814, "type": "U16", "scale": 0.1},
            "GRID_CURR": {"address": 0x3817, "type": "S16", "scale": 0.01},
            "GRID_FREQ": {"address": 0x381A, "type": "U16", "scale": 0.01},
            "LOAD_PWR": {"address": 0x381C, "type": "U16", "scale": 0.1},
            "ACTIVE_PWR": {"address": 0x381D, "type": "S32", "scale": 0.1},
            "REACTIVE_PWR": {"address": 0x381F, "type": "S32", "scale": 0.1},
            "INVT_TEMP": {"address": 0x3822, "type": "S16", "scale": 0.1},
            "AMBIENT_TEMP": {"address": 0x3825, "type": "S16", "scale": 0.1},
            "RADIATOR_TEMP": {"address": 0x3826, "type": "S16", "scale": 0.1},
            "METER_PWR": {"address": 0x3827, "type": "S32", "scale": 0.1},
            "LEAKAGE_CURR": {"address": 0x3829, "type": "S16", "scale": 0.1},
            "DERAT_PWR": {"address": 0x382A, "type": "U32", "scale": 0.1},
            "DERAT_MODE": {"address": 0x382C, "type": "U16", "scale": 0.1},
            "PV_EN_DAY": {"address": 0x382F, "type": "U16", "scale": 0.1},
            "DC_OHM": {"address": 0x3835, "type": "U16", "scale": 1},
            "PV1_V": {"address": 0x3836, "type": "U16", "scale": 0.1},
            "PV1_CURR": {"address": 0x3837, "type": "S16", "scale": 0.01},
            "PV2_V": {"address": 0x3838, "type": "U16", "scale": 0.1},
            "PV2_CURR": {"address": 0x3839, "type": "S16", "scale": 0.01},
            "CT_CURR": {"address": 0x3839, "type": "S16", "scale": 0.01},
            "LOAD_EN_DAY": {"address": 0x3892, "type": "U16", "scale": 0.1},
            "LOAD_EN_TOTAL": {"address": 0x3893, "type": "U32", "scale": 0.1},
            "EXPORT_EN_DAY": {"address": 0x3895, "type": "U16", "scale": 0.1},
            "EXPORT_EN_TOTAL": {"address": 0x3896, "type": "U32", "scale": 0.1},
            "IMPORT_EN_DAY": {"address": 0x3898, "type": "U16", "scale": 0.1},
            "IMPORT_EN_TOTAL": {"address": 0x3899, "type": "U32", "scale": 0.1},
            "BAT+_DAY": {"address": 0x389B, "type": "U16", "scale": 0.1},
            "BAT+_TOTAL": {"address": 0x389C, "type": "U32", "scale": 0.1},
            "BAT-_DAY": {"address": 0x389E, "type": "U16", "scale": 0.1},
            "BAT-_TOTAL": {"address": 0x389F, "type": "U32", "scale": 0.1},
            "BAT_PWR": {"address": 0x3908, "type": "S32", "scale": 0.1},
            "BAT_V": {"address": 0x390A, "type": "U16", "scale": 0.1},
            "BAT_CURR": {"address": 0x390B, "type": "S16", "scale": 0.1},
            "EPS_PWR": {"address": 0x3929, "type": "S32", "scale": 0.1},
            "BAT_SOC": {"address": 0x393B, "type": "U16", "scale": 1},
            "BAT_SOH": {"address": 0x393C, "type": "U16", "scale": 1},
            "BAT_TEMP": {"address": 0x394D, "type": "U16", "scale": 0.1},
            "PV1_PWR": {"address": 0x3B01, "type": "U16", "scale": 0.1},
            "PV2_PWR": {"address": 0x3B02, "type": "U16", "scale": 0.1}
        }

        while True:
            results = {}

            for sensor, config in sensors.items():
                try:
                    value = read_sensor_value(
                        client,
                        config['address'],
                        slave=1,
                        data_type=config['type'],
                        scale=config['scale']
                    )
                    results[sensor] = value
                except Exception as e:
                    results[sensor] = f"Error: {e}"

            json_payload = json.dumps({k: float(v) if isinstance(v, np.generic) else v for k, v in results.items()})
            mqtt_client.publish(os.getenv("MQTT_TOPIC"), json_payload)

            # Debug print
            print(f"Published: {json_payload}")

            mqtt_client.loop(2)  # Maintain network loop for MQTT
            time.sleep(int(os.getenv("UPDATE_INTERVAL")))

    except Exception as e:
        print(e)
    finally:
        client.close()

if __name__ == "__main__":
    main()