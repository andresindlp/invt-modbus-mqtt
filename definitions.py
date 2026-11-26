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
        "address": 0x3927,
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
        "unit": "var"
    },
    "INVT_TEMP": {
        "address": 0x3822,
        "type": "S16",
        "scale": 0.1,
        "unit": "°C"
    },
    "AMBIENT_TEMP": {
        "address": 0x3825,
        "type": "S16",
        "scale": 0.1,
        "unit": "°C"
    },
    "RADIATOR_TEMP": {
        "address": 0x3826,
        "type": "S16",
        "scale": 0.1,
        "unit": "°C"
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
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "No Derating",
            1: "High Voltage Derating",
            2: "Boost High Temperature Derating",
            3: "Inverter Derating",
            4: "Ambient Temperature Derating",
            5: "Power Setting Derating",
            6: "Reset MPPT Derating",
            7: "Reactive Power Derating",
            8: "Loading Slope Derating",
            9: "AC High Voltage Derating",
            10: "ATE Adjust Derating",
            11: "Single Inverter Anti-reflux Derating",
            12: "Multi-inverter Anti-reflux Derating",
            13: "Over-frequency Derating"
        }
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
        "unit": "°C"
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
    },
    "PV_EN_TOTAL": {
        "address": 0x3830,
        "type": "U32",
        "scale": 0.1,
        "unit": "kWh"
    },
    "PV_TOTAL_PWR": {
        "address": 0x38E4,
        "type": "U32",
        "scale": 1,
        "unit": "W"
    },
    "POWER_FACTOR": {
        "address": 0x3821,
        "type": "S16",
        "scale": 0.001,
        "unit": ""
    },
    "POWER_GEN_TIME": {
        "address": 0x382D,
        "type": "U32",
        "scale": 0.5,
        "unit": "s"
    },
    "INVERTER_STATUS": {
        "address": 0x3806,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Initialization",
            1: "Wait",
            2: "On-grid",
            3: "Fault",
            4: "Burning Program",
            5: "Off-grid",
            6: "Bypass",
            7: "PID Repair",
            8: "PID Inhibition",
            9: "Snow Removal",
            10: "SVG Mode"
        }
    },
    "MAIN_ALARM_CODE": {
        "address": 0x3807,
        "type": "U16",
        "scale": 1,
        "unit": ""
    },
    "SUB_ALARM_CODE": {
        "address": 0x3808,
        "type": "U16",
        "scale": 1,
        "unit": ""
    },
    "MAIN_FAULT_CODE": {
        "address": 0x3809,
        "type": "U16",
        "scale": 1,
        "unit": ""
    },
    "SUB_FAULT_CODE": {
        "address": 0x380A,
        "type": "U16",
        "scale": 1,
        "unit": ""
    },
    "GRID_CONNECT_COUNTDOWN": {
        "address": 0x381B,
        "type": "U16",
        "scale": 1,
        "unit": "s"
    },
    "BAT_STATUS": {
        "address": 0x3924,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Idle",
            1: "Charging",
            2: "Discharging"
        }
    },
    "BMS_MAX_CHG_CURR": {
        "address": 0x3939,
        "type": "U16",
        "scale": 0.1,
        "unit": "A"
    },
    "BMS_MAX_DSG_CURR": {
        "address": 0x393A,
        "type": "U16",
        "scale": 0.1,
        "unit": "A"
    },
    "BMS_COMM_STATUS": {
        "address": 0x394C,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Abnormal",
            1: "Normal"
        }
    },
    "BMS_MODULE_STATUS": {
        "address": 0x393F,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Normal",
            1: "Prompt",
            2: "Warning",
            3: "Fault"
        }
    },
    "BMS_CHG_DISABLE": {
        "address": 0x393D,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Allowed",
            1: "Prohibited"
        }
    },
    "BMS_DSG_DISABLE": {
        "address": 0x393E,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Allowed",
            1: "Prohibited"
        }
    },
    "EPS_CURR": {
        "address": 0x3928,
        "type": "U16",
        "scale": 0.01,
        "unit": "A"
    },
    "EPS_FREQ": {
        "address": 0x3926,
        "type": "U16",
        "scale": 0.01,
        "unit": "Hz"
    },
    "PRIORITY_MODE": {
        "address": 0x3111,
        "type": "U16",
        "scale": 1,
        "unit": "",
        "value_map": {
            0: "Load Priority",
            1: "Battery Priority",
            2: "Grid Priority"
        }
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
        "device_class": "enum"
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
    "PV_EN_TOTAL": {
        "name": "Total PV Energy",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing"
    },
    "PV_TOTAL_PWR": {
        "name": "Total PV Power",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement"
    },
    "POWER_FACTOR": {
        "name": "Power Factor",
        "icon": "mdi:angle-acute",
        "device_class": "power_factor",
        "state_class": "measurement"
    },
    "POWER_GEN_TIME": {
        "name": "Total Generation Time",
        "icon": "mdi:timer-outline",
        "device_class": "duration",
        "state_class": "total_increasing"
    },
    "INVERTER_STATUS": {
        "name": "Inverter Status",
        "icon": "mdi:state-machine",
        "device_class": "enum"
    },
    "MAIN_ALARM_CODE": {
        "name": "Main Alarm Code",
        "icon": "mdi:alert-outline"
    },
    "SUB_ALARM_CODE": {
        "name": "Sub Alarm Code",
        "icon": "mdi:alert-outline"
    },
    "MAIN_FAULT_CODE": {
        "name": "Main Fault Code",
        "icon": "mdi:alert-octagon-outline"
    },
    "SUB_FAULT_CODE": {
        "name": "Sub Fault Code",
        "icon": "mdi:alert-octagon-outline"
    },
    "GRID_CONNECT_COUNTDOWN": {
        "name": "Grid Connect Countdown",
        "icon": "mdi:timer-sand",
        "device_class": "duration",
        "state_class": "measurement"
    },
    "BAT_STATUS": {
        "name": "Battery Status",
        "icon": "mdi:battery-sync",
        "device_class": "enum"
    },
    "BMS_MAX_CHG_CURR": {
        "name": "BMS Max Charge Current",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement"
    },
    "BMS_MAX_DSG_CURR": {
        "name": "BMS Max Discharge Current",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement"
    },
    "BMS_COMM_STATUS": {
        "name": "BMS Communication Status",
        "icon": "mdi:lan-connect",
        "device_class": "enum"
    },
    "BMS_MODULE_STATUS": {
        "name": "BMS Module Status",
        "icon": "mdi:battery-check",
        "device_class": "enum"
    },
    "BMS_CHG_DISABLE": {
        "name": "BMS Charging Permission",
        "icon": "mdi:battery-charging",
        "device_class": "enum"
    },
    "BMS_DSG_DISABLE": {
        "name": "BMS Discharging Permission",
        "icon": "mdi:battery-arrow-down",
        "device_class": "enum"
    },
    "EPS_CURR": {
        "name": "EPS Current",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement"
    },
    "EPS_FREQ": {
        "name": "EPS Frequency",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement"
    },
    "PRIORITY_MODE": {
        "name": "Priority Mode",
        "icon": "mdi:tune",
        "device_class": "enum"
    },
    "FAULT_STATUS": {
        "name": "Fault Status",
        "icon": "mdi:alert-octagon",
        "device_class": "enum"
    },
    "ALARM_STATUS": {
        "name": "Alarm Status",
        "icon": "mdi:alert",
        "device_class": "enum"
    },
}

derived_sensors = ["FAULT_STATUS", "ALARM_STATUS"]

FAULT_TYPES = {
    1: "PV voltage error",
    3: "BUS voltage error",
    5: "Over-current",
    6: "Temperature error",
    7: "Insulation monitoring error",
    8: "Driver error",
    9: "Communication error",
    10: "Leakage current error",
    11: "Relay failure",
    12: "Internal fan failure",
    14: "DCI error",
    15: "PID failure",
    19: "Consistency error",
    31: "AC voltage error",
    33: "AC frequency error",
    36: "Model identification failure",
    37: "Remote shutdown",
    38: "AFCI error",
    39: "AFCI self-test error",
    40: "Parallel fault",
    41: "AutoTest failure",
    42: "N-PE fault",
    43: "Leakage current self-test error",
    44: "PV string detection error",
    45: "Auxiliary power error",
    46: "EPS short circuit",
    47: "Battery fault (level 1)",
    48: "Battery fault (level 2)",
    49: "Battery fault (level 3)",
}

FAULT_CODES = {
    (1, 1): "Low PV voltage",
    (1, 2): "High PV voltage",
    (1, 3): "Short circuit of PV panel",
    (1, 4): "PV1 short circuit",
    (1, 5): "PV2 short circuit",
    (1, 6): "PV1 reverse polarity connection",
    (1, 7): "PV2 reverse polarity connection",
    (3, 1): "Low BUS voltage",
    (3, 2): "High BUS voltage",
    (3, 3): "BUS voltage unbalance",
    (3, 4): "Hardware BUS over-voltage",
    (5, 1): "Inverter hardware over-current",
    (5, 2): "Inverter software over-current",
    (5, 3): "Boost hardware over-current",
    (5, 4): "Boost software over-current",
    (5, 5): "Auxiliary power hardware TZ failure",
    (5, 6): "BUS hardware TZ over-voltage",
    (5, 7): "Hardware TZ failure at LLC side",
    (5, 8): "Buck-boost software over-current",
    (6, 1): "Abnormal inverter temperature",
    (6, 2): "Abnormal boost temperature",
    (6, 3): "Abnormal radiator temperature",
    (6, 4): "Abnormal ambient temperature",
    (6, 5): "Abnormal buck-boost temperature",
    (6, 6): "NTC thermistor open circuit",
    (7, 1): "Insulation monitoring error",
    (8, 1): "Driver error",
    (9, 1): "Communication error from ARM to master DSP",
    (9, 2): "Communication error from master DSP to ARM",
    (9, 3): "Communication error from ARM to slave DSP",
    (9, 4): "Communication error from slave DSP to ARM",
    (9, 5): "Master-slave chip communication error (master chip)",
    (9, 6): "Master-slave chip communication error (slave chip)",
    (9, 7): "Communication error between DSP and AFCI",
    (10, 1): "High static leakage current",
    (10, 2): "Abrupt leakage current fault (30mA)",
    (10, 3): "Abrupt leakage current fault (60mA)",
    (10, 4): "Abrupt leakage current fault (150mA)",
    (11, 1): "Relay open circuit",
    (11, 2): "Relay short circuit",
    (12, 1): "Internal fan failure",
    (14, 1): "R-phase DCI error",
    (14, 2): "S-phase DCI error",
    (14, 3): "T-phase DCI error",
    (15, 1): "PID BUS voltage high",
    (19, 1): "Inconsistent AC voltage values",
    (19, 2): "Inconsistent BUS voltage values",
    (19, 3): "Inconsistent ISO voltage values",
    (19, 4): "Inconsistent PV voltage values",
    (19, 5): "Inconsistent GFCI values",
    (19, 6): "BUS voltage sampling error",
    (19, 7): "PV current sampling error",
    (31, 1): "AC level-1 under-voltage",
    (31, 2): "AC level-1 over-voltage",
    (31, 3): "No AC voltage",
    (31, 4): "AC level-2 under-voltage",
    (31, 5): "AC level-2 over-voltage",
    (31, 6): "AC startup under-voltage",
    (31, 7): "AC startup over-voltage",
    (31, 8): "Transient interrupt over-voltage",
    (31, 9): "Islanding over-voltage",
    (31, 10): "Grid voltage oscillation",
    (31, 11): "AC level-3 under-voltage",
    (31, 12): "Grid voltage phase lock fault",
    (33, 1): "AC level-1 under-frequency",
    (33, 2): "AC level-1 over-frequency",
    (33, 3): "AC level-2 under-frequency",
    (33, 4): "AC level-2 over-frequency",
    (33, 5): "AC startup under-frequency",
    (33, 6): "AC startup over-frequency",
    (33, 7): "Frequency self-test failed",
    (36, 1): "Model identification failure",
    (37, 1): "Remote shutdown command",
    (37, 2): "Under maintenance",
    (38, 1): "AFCI failure on PV string 1",
    (38, 2): "AFCI failure on PV string 2",
    (39, 1): "AFCI self-test error on PV string 1",
    (39, 2): "AFCI self-test error on PV string 2",
    (40, 1): "Multiple host failure",
    (40, 2): "Parallel CAN communication failure",
    (40, 3): "Host loss fault",
    (40, 4): "Synchronous zero-crossing fault",
    (41, 1): "AutoTest failure",
    (42, 1): "N-PE voltage error",
    (43, 1): "Leakage current sensor failure",
    (44, 1): "PV string failure",
    (45, 1): "Auxiliary power failure",
    (46, 1): "Short circuit of EPS",
    (47, 1): "Battery charging temperature low (level 1)",
    (47, 2): "Battery charging temperature high (level 1)",
    (47, 3): "Battery discharge temperature low (level 1)",
    (47, 4): "Battery discharge temperature high (level 1)",
    (47, 5): "Large cell voltage difference (level 1)",
    (47, 6): "Large cell temperature difference (level 1)",
    (47, 7): "Battery power too low",
    (47, 8): "Battery health too low (level 1)",
    (47, 9): "Single cell voltage low (level 1)",
    (47, 10): "Single cell voltage high (level 1)",
    (47, 11): "Battery charging current high (level 1)",
    (47, 12): "Battery discharge current high (level 1)",
    (47, 13): "Battery charging power high (level 1)",
    (47, 14): "Battery discharge power high (level 1)",
    (47, 15): "Battery total voltage low (level 1)",
    (47, 16): "Battery total voltage high (level 1)",
    (48, 1): "Battery discharge temperature low (level 2)",
    (48, 2): "Battery discharge temperature high (level 2)",
    (48, 3): "Large cell voltage difference (level 2)",
    (48, 4): "Large cell temperature difference (level 2)",
    (48, 5): "Battery internal communication failure",
    (48, 6): "Battery external communication failure",
    (48, 7): "Battery precharge failure",
    (48, 8): "Battery parallel failure",
    (48, 9): "Single cell voltage low (level 2)",
    (48, 10): "Single cell voltage high (level 2)",
    (48, 11): "Battery charging current high (level 2)",
    (48, 12): "Battery charging power high (level 2)",
    (48, 13): "Battery discharge current high (level 2)",
    (48, 14): "Battery discharge power high (level 2)",
    (48, 15): "Battery charging temperature low (level 2)",
    (48, 16): "Battery charging temperature high (level 2)",
    (49, 1): "Battery voltage too low",
    (49, 2): "Large cell voltage difference (level 3)",
    (49, 3): "Single cell voltage high (level 3)",
    (49, 4): "Single cell temperature too high",
    (49, 5): "Charger voltage high",
    (49, 6): "Battery health too low (level 2)",
    (49, 7): "Battery total voltage low (level 2)",
    (49, 8): "Battery total voltage high (level 2)",
    (49, 9): "BMS hardware failure",
    (49, 10): "ACTOR adjoin failure",
    (49, 11): "Battery short circuit fault",
    (49, 12): "AFE and MCU communication failure",
    (49, 13): "EEPROM and MCU communication failure",
    (49, 14): "ACTOR driver failure",
    (49, 15): "Battery fuse failure",
    (49, 16): "Battery internal fault",
}

ALARM_TYPES = {
    1: "Low fan speed",
    2: "Lightning protector alarm",
    4: "Anti-reflux meter communication",
    5: "Out-of-range grid voltage",
    6: "Short circuit of PV",
    7: "EPS overload alarm",
    8: "Fuse abnormality alarm",
    9: "AC coupling meter alarm",
    46: "Full battery",
    47: "Low battery voltage",
    48: "Battery alarm",
}

ALARM_CODES = {
    (1, 7): "Internal fan 1 speed low",
    (1, 8): "Internal fan 2 speed low",
    (1, 11): "Fan speed low",
    (2, 1): "DC lightning protector alarm",
    (2, 2): "AC lightning protector alarm",
    (4, 1): "Meter failure",
    (4, 8): "Communication error of meter",
    (4, 16): "CT cable error",
    (4, 32): "Meter identification abnormality",
    (5, 0): "Out-of-range grid voltage",
    (6, 1): "Short circuit of PV2",
    (6, 2): "Short circuit of PV1",
    (7, 1): "EPS overload (power exceeds 1.5x)",
    (7, 2): "EPS overload (power exceeds 1.2x)",
    (7, 3): "EPS overload (power exceeds 1.1x)",
    (7, 4): "EPS overload (current exceeds 1.5x)",
    (7, 5): "EPS overload (current exceeds 1.2x)",
    (7, 6): "EPS overload (current exceeds 1.1x)",
    (8, 1): "Fuse abnormality alarm",
    (9, 1): "Meter 1 communication abnormality",
    (9, 2): "Meter 2 communication abnormality",
    (9, 3): "Meter 1 and Meter 2 communication abnormality",
    (46, 1): "Full battery",
    (47, 1): "Battery needs to be charged",
    (47, 2): "Battery can only be charged",
    (48, 1): "Low temperature alarm during battery charging",
    (48, 2): "High temperature alarm during battery charging",
    (48, 3): "Low temperature alarm during battery discharging",
    (48, 4): "High temperature alarm during battery discharging",
    (48, 5): "Large cell voltage difference alarm",
    (48, 6): "Large cell temperature difference alarm",
    (48, 7): "Battery power low alarm",
    (48, 8): "Battery health too low alarm",
    (48, 9): "Single cell low voltage alarm",
    (48, 10): "Single cell high voltage alarm",
    (48, 11): "Battery charging current high alarm",
    (48, 12): "Battery discharge current high alarm",
    (48, 13): "Battery charging power high alarm",
    (48, 14): "Battery discharge power high alarm",
    (48, 15): "Low total battery voltage alarm",
    (48, 16): "High total battery voltage alarm",
    (48, 17): "Abnormal battery status",
}

device_info = {
    "identifiers": ["invt_001"],
    "name": "INVT",
    "manufacturer": "INVT",
    "model": "XD6KTL",
    "hw_version": "V1.0",
}