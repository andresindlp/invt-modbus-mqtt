# INVT Solar Inverter Modbus-MQTT Publisher

This project is designed to read data from an INVT solar inverter using Modbus and publish the readings to an MQTT broker.

## Features

- **Modbus Communication**: Retrieve data directly from the INVT solar inverter.
- **MQTT Publishing**: Transmit inverter data to an MQTT broker for further analysis or integration.
- **Environment Configurations**: Use a `.env` file to manage configurations securely.

## Prerequisites

Ensure you have the following:

- [RS485 to ETH adapter](https://www.waveshare.com/wiki/RS485_TO_ETH_(B)). Follow [this](https://homeassistant-solax-modbus.readthedocs.io/en/latest/modbus-adaptor-setup/) guide to set it up.
- Python>3.9 and an MQTT Broker already set up.

## COM Port Wiring
We only need A+ and B-, which on INVT inverters with a round COM port are PINs 2 and 3. The PINs are written inside the connector. I've used alligator clips and a 120 Ohm resistor on both ends of the chain (not necessary)

> [!WARNING]  
> Be careful connecting the adapter to the COM port, the PINs are very close together and you can short out your inverter. I'm not responsible for any damages that may occur.

> [!TIP]
> If you wish to maintain Solarman connectivity, enable RS485 on COM2 through the app, then plug the data logger in COM2, leaving COM1 for the ETH adapter. In my testing they work fine together.



## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/andresindlp/invt-modbus-mqtt.git
   cd invt-modbus-mqtt
   ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables**:
   ```bash
    mv .env.example .env
    nano .env
    ```
    Be mindful when setting up the update interval to not overload the inverter's bus, I've found 5 seconds works well.

4. **Run the script**:
   ```bash
    python3 main.py
    ```

## Example output

```json
{
    "EPS_V": 230,
    "PBUS_V": 388.2,
    "GRID_V": 240,
    "GRID_CURR": 0.67,
    "GRID_FREQ": 50.04,
    "LOAD_PWR": 0.2,
    "ACTIVE_PWR": 154.5,
    "REACTIVE_PWR": 48.1,
    "INVT_TEMP": 28.5,
    "AMBIENT_TEMP": 58.5,
    "RADIATOR_TEMP": 29.9,
    "METER_PWR": 7.2,
    "LEAKAGE_CURR": 13.5,
    "DERAT_PWR": 6050,
    "DERAT_MODE": 0,
    "PV_EN_DAY": 0,
    "DC_OHM": 3029,
    "PV1_V": 12.8,
    "PV1_CURR": 0.01,
    "PV2_V": 13,
    "PV2_CURR": 0.01,
    "CT_CURR": 0.01,
    "LOAD_EN_DAY": 0.1,
    "LOAD_EN_TOTAL": 126.4,
    "EXPORT_EN_DAY": 0,
    "EXPORT_EN_TOTAL": 221.2,
    "IMPORT_EN_DAY": 0,
    "IMPORT_EN_TOTAL": 15.7,
    "BAT+_DAY": 0,
    "BAT+_TOTAL": 51.7,
    "BAT-_DAY": 0.1,
    "BAT-_TOTAL": 45,
    "BAT_PWR": -201.2,
    "BAT_V": 49.5,
    "BAT_CURR": -4,
    "EPS_PWR": 61.9,
    "BAT_SOC": 68,
    "BAT_SOH": 100,
    "BAT_TEMP": 18.7,
    "PV1_PWR": 0.1,
    "PV2_PWR": 0.1
}
```

## Acknowledgments
- [homeassistant-solax-modbus](https://github.com/wills106/homeassistant-solax-modbus) for their amazing documentation.
- [MrLopHA](https://github.com/MrLopHA) for their valuable contributions and inspiration.