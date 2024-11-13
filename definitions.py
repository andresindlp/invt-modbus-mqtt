from dotenv import load_dotenv
import os

load_dotenv()

## TIP: Use U32 to join two U16 registers.
## Example: 

# +--------+------------------------------------------+---+---+-----+-----+----+
# | 0x3899 | Total purchased electricity (HIGH 16 bits)| 1 | R | 0.1 | kWh | U16|
# +--------+------------------------------------------+---+---+-----+-----+----+
# | 0x389A | Total purchased electricity (LOW 16 bits) | 1 | R | 0.1 | kWh | U16|
# +--------+------------------------------------------+---+---+-----+-----+----+

# The resulting code would be:
# "IMPORT_EN_TOTAL": {
#         "address": 0x3899,  <----- "High 16 bits"
#         "type": "U32",  <----- Specifying U32 = High 16 + Low 16
#         "scale": 0.1,
#         "unit": "kWh"
#     }


sensors = {
    "EPS_V": {
        "address": 0x3115,
        "type": "U16",
        "scale": 0.1,
        "unit": "V"
    },
    "PBUS_V": {
        "address": 0x380F,
        "type": "U16",
        "scale": 0.1,
        "unit": "V"
    },
    "GRID_V": {
        "address": 0x3814,
        "type": "U16",
        "scale": 0.1,
        "unit": "V"
    },
    "GRID_CURR": {
        "address": 0x3817,
        "type": "S16",
        "scale": 0.01,
        "unit": "A"
    },
    "GRID_FREQ": {
        "address": 0x381A,
        "type": "U16",
        "scale": 0.01,
        "unit": "Hz"
    },
    "LOAD_PWR": {
        "address": 0x381C,
        "type": "U16",
        "scale": 0.1,
        "unit": "kW"
    },
    "ACTIVE_PWR": {
        "address": 0x381D,
        "type": "S32",
        "scale": 0.1,
        "unit": "W"
    },
    "REACTIVE_PWR": {
        "address": 0x381F,
        "type": "S32",
        "scale": 0.1,
        "unit": "Var"
    },
    "INVT_TEMP": {
        "address": 0x3822,
        "type": "S16",
        "scale": 0.1,
        "unit": "ºC"
    },
    "AMBIENT_TEMP": {
        "address": 0x3825,
        "type": "S16",
        "scale": 0.1,
        "unit": "ºC"
    },
    "RADIATOR_TEMP": {
        "address": 0x3826,
        "type": "S16",
        "scale": 0.1,
        "unit": "ºC"
    },
    "METER_PWR": {
        "address": 0x3827,
        "type": "S32",
        "scale": 0.1,
        "unit": "W"
    },
    "LEAKAGE_CURR": {
        "address": 0x3829,
        "type": "S16",
        "scale": 0.1,
        "unit": "mA"
    },
    "DERAT_PWR": {
        "address": 0x382A,
        "type": "U32",
        "scale": 0.1,
        "unit": "W"
    },
    "DERAT_MODE": {
        "address": 0x382C,
        "type": "U16",
        "scale": 0.1,
        "unit": ""
    },
    "PV_EN_DAY": {
        "address": 0x382F,
        "type": "U16",
        "scale": 0.1,
        "unit": "kWh"
    },
    "DC_OHM": {
        "address": 0x3835,
        "type": "U16",
        "scale": 1,
        "unit": "kΩ"
    },
    "PV1_V": {
        "address": 0x3836,
        "type": "U16",
        "scale": 0.1,
        "unit": "V"
    },
    "PV1_CURR": {
        "address": 0x3837,
        "type": "S16",
        "scale": 0.01,
        "unit": "A"
    },
    "PV2_V": {
        "address": 0x3838,
        "type": "U16",
        "scale": 0.1,
        "unit": "V"
    },
    "PV2_CURR": {
        "address": 0x3839,
        "type": "S16",
        "scale": 0.01,
        "unit": "A"
    },
    "CT_CURR": {
        "address": 0x3839,
        "type": "S16",
        "scale": 0.01,
        "unit": "A"
    },
    "LOAD_EN_DAY": {
        "address": 0x3892,
        "type": "U16",
        "scale": 0.1,
        "unit": "kWh"
    },
    "LOAD_EN_TOTAL": {
        "address": 0x3893,
        "type": "U32",
        "scale": 0.1,
        "unit": "kWh"
    },
    "EXPORT_EN_DAY": {
        "address": 0x3895,
        "type": "U16",
        "scale": 0.1,
        "unit": "kWh"
    },
    "EXPORT_EN_TOTAL": {
        "address": 0x3896,
        "type": "U32",
        "scale": 0.1,
        "unit": "kWh"
    },
    "IMPORT_EN_DAY": {
        "address": 0x3898,
        "type": "U16",
        "scale": 0.1,
        "unit": "kWh"
    },
    "IMPORT_EN_TOTAL": {
        "address": 0x3899,
        "type": "U32",
        "scale": 0.1,
        "unit": "kWh"
    },
    "BAT_CHARGE_DAY": {
        "address": 0x389B,
        "type": "U16",
        "scale": 0.1,
        "unit": "kWh"
    },
    "BAT_CHARGE_TOTAL": {
        "address": 0x389C,
        "type": "U32",
        "scale": 0.1,
        "unit": "kWh"
    },
    "BAT_DISCARGE_DAY": {
        "address": 0x389E,
        "type": "U16",
        "scale": 0.1,
        "unit": "kWh"
    },
    "BAT_DISCHARGE_TOTAL": {
        "address": 0x389F,
        "type": "U32",
        "scale": 0.1,
        "unit": "kWh"
    },
    "BAT_PWR": {
        "address": 0x3908,
        "type": "S32",
        "scale": 0.1,
        "unit": "W"
    },
    "BAT_V": {
        "address": 0x390A,
        "type": "U16",
        "scale": 0.1,
        "unit": "V"
    },
    "BAT_CURR": {
        "address": 0x390B,
        "type": "S16",
        "scale": 0.1,
        "unit": "A"
    },
    "EPS_PWR": {
        "address": 0x3929,
        "type": "S32",
        "scale": 0.1,
        "unit": "W"
    },
    "BAT_SOC": {
        "address": 0x393B,
        "type": "U16",
        "scale": 1,
        "unit": "%"
    },
    "BAT_SOH": {
        "address": 0x393C,
        "type": "U16",
        "scale": 1,
        "unit": "%"
    },
    "BAT_TEMP": {
        "address": 0x394D,
        "type": "U16",
        "scale": 0.1,
        "unit": "ºC"
    },
    "PV1_PWR": {
        "address": 0x3B01,
        "type": "U16",
        "scale": 0.1,
        "unit": "W"
    },
    "PV2_PWR": {
        "address": 0x3B02,
        "type": "U16",
        "scale": 0.1,
        "unit": "W"
    }
}

sensor_details = {
    "EPS_V": {
        "name": "EPS Voltage",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "PBUS_V": {
        "name": "PBUS Voltage",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "GRID_V": {
        "name": "Grid Voltage",
        "icon": "mdi:transmission-tower",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "GRID_CURR": {
        "name": "Grid Current",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement"
    },
    "GRID_FREQ": {
        "name": "Grid Frequency",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement"
    },
    "LOAD_PWR": {
        "name": "Load Power",
        "icon": "mdi:power-plug",
        "device_class": "power",
        "state_class": "measurement"
    },
    "ACTIVE_PWR": {
        "name": "Active Power",
        "icon": "mdi:lightning-bolt-circle",
        "device_class": "power",
        "state_class": "measurement"
    },
    "REACTIVE_PWR": {
        "name": "Reactive Power",
        "icon": "mdi:flash-off",
        "device_class": "reactive_power",
        "state_class": "measurement"
    },
    "INVT_TEMP": {
        "name": "Inverter Temperature",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "AMBIENT_TEMP": {
        "name": "Ambient Temperature",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "RADIATOR_TEMP": {
        "name": "Radiator Temperature",
        "icon": "mdi:radiator",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "METER_PWR": {
        "name": "Power Meter",
        "icon": "mdi:meter-electric",
        "device_class": "power",
        "state_class": "measurement"
    },
    "LEAKAGE_CURR": {
        "name": "Leakage Current",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement"
    },
    "DERAT_PWR": {
        "name": "Derated Power",
        "icon": "mdi:power-settings",
        "device_class": "power",
        "state_class": "measurement"
    },
    "DERAT_MODE": {
        "name": "Derating Mode",
        "icon": "mdi:alert-circle",
        "device_class": "enum",
        "state_class": "measurement"
    },
    "PV_EN_DAY": {
        "name": "PV Energy Today",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "DC_OHM": {
        "name": "DC Isolation Resistance",
        "icon": "mdi:resistor",
        "device_class": "power",
        "state_class": "measurement"
    },
    "PV1_V": {
        "name": "PV1 Voltage",
        "icon": "mdi:solar-power",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "PV1_CURR": {
        "name": "PV1 Current",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement"
    },
    "PV2_V": {
        "name": "PV2 Voltage",
        "icon": "mdi:solar-power",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "PV2_CURR": {
        "name": "PV2 Current",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement"
    },
    "CT_CURR": {
        "name": "CT Current",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement"
    },
    "LOAD_EN_DAY": {
        "name": "Load Energy Today",
        "icon": "mdi:power-plug",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "LOAD_EN_TOTAL": {
        "name": "Total Load Energy",
        "icon": "mdi:power-plug",
        "device_class": "energy",
        "state_class": "total"
    },
    "EXPORT_EN_DAY": {
        "name": "Export Energy Today",
        "icon": "mdi:home-export-outline",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "EXPORT_EN_TOTAL": {
        "name": "Total Export Energy",
        "icon": "mdi:home-export-outline",
        "device_class": "energy",
        "state_class": "total"
    },
    "IMPORT_EN_DAY": {
        "name": "Import Energy Today",
        "icon": "mdi:home-import-outline",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "IMPORT_EN_TOTAL": {
        "name": "Total Import Energy",
        "icon": "mdi:home-import-outline",
        "device_class": "energy",
        "state_class": "total"
    },
    "BAT_CHARGE_DAY": {
        "name": "Battery Charge Today",
        "icon": "mdi:battery-plus-outline",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "BAT_CHARGE_TOTAL": {
        "name": "Total Battery Charge",
        "icon": "mdi:battery-plus-outline",
        "device_class": "energy",
        "state_class": "total"
    },
    "BAT_DISCARGE_DAY": {
        "name": "Battery Discharge Today",
        "icon": "mdi:battery-minus-outline",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "BAT_DISCHARGE_TOTAL": {
        "name": "Total Battery Discharge",
        "icon": "mdi:battery-minus-outline",
        "device_class": "energy",
        "state_class": "total"
    },
    "BAT_PWR": {
        "name": "Battery Power",
        "icon": "mdi:battery-outline",
        "device_class": "power",
        "state_class": "measurement"
    },
    "BAT_V": {
        "name": "Battery Voltage",
        "icon": "mdi:battery-outline",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "BAT_CURR": {
        "name": "Battery Current",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement"
    },
    "EPS_PWR": {
        "name": "EPS Power",
        "icon": "mdi:power-plug",
        "device_class": "power",
        "state_class": "measurement"
    },
    "BAT_SOC": {
        "name": "Battery State of Charge",
        "icon": "mdi:battery",
        "device_class": "battery",
        "state_class": "measurement"
    },
    "BAT_SOH": {
        "name": "Battery State of Health",
        "icon": "mdi:battery-heart",
        "device_class": "battery",
        "state_class": "measurement"
    },
    "BAT_TEMP": {
        "name": "Battery Temperature",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "PV1_PWR": {
        "name": "PV1 Power",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement"
    },
    "PV2_PWR": {
        "name": "PV2 Power",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement"
    },
}

device_info = {
            "identifiers": ["invt_001"],
            "name": "INVT",
            "manufacturer": "INVT",
            "model": "XD6KTL",
            "sw_version": "425-422-0-101",
            "hw_version": "V1.0",
            "serial_number": os.getenv("INVT_SERIAL_NUMBER")
        }