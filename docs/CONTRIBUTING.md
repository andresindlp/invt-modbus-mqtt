# Contributing

Thanks for your interest in contributing to **invt-modbus-mqtt**!

Contributions are welcome, whether you are fixing documentation, adding support for additional registers, improving Home Assistant integration, fixing bugs, or sharing information about other compatible INVT inverter models.

Before submitting a pull request, please keep the following points in mind.

## General Guidelines

- Keep changes focused. If possible, avoid combining unrelated changes into the same pull request.
- Explain clearly what your change does and why it is needed.
- Test code changes with your setup before submitting them.
- Avoid committing credentials, MQTT passwords, IP addresses, or other private information.
- Do not commit your `.env` file. Use `.env.example` when documenting new configuration options.
- Try to preserve backwards compatibility unless there is a good reason not to.
- If you are unsure whether a larger change fits the project, feel free to open an issue first to discuss it.

## Hardware Safety

This project communicates directly with solar inverter hardware.

Please be careful when testing changes involving Modbus communication, register writes, polling intervals, or physical wiring.

Unless explicitly documented otherwise, contributions should assume that Modbus access is **read-only**. Avoid introducing writes to inverter registers without a clear reason, documentation, and appropriate safeguards.

Incorrect wiring, register access, or communication settings may cause unexpected behavior or damage equipment. Test hardware-related changes carefully.

## Modbus Registers

Register definitions are kept in `definitions.py`.

When adding or correcting a register, please include as much information as possible about where the register information came from. For example:

- INVT documentation or register maps
- The inverter model and firmware version you tested
- Comparison with another implementation
- Results observed directly from your inverter

If a register appears to behave differently between inverter models or firmware versions, mention that in your pull request.

Do not assume a register is universally compatible simply because it works on one inverter.

## Supported Hardware

The project was created for **INVT XD series 3–6 kW inverters**.

Contributions related to other INVT models are welcome, but please clearly state:

- The exact inverter model
- Firmware version, if known
- Which functionality you have tested
- Any registers or behavior that differ from the currently supported models

This information can help determine whether a change should become part of the default definitions or require model-specific handling.

## MQTT and Home Assistant

When changing MQTT topics, payloads, sensor names, units, device classes, or Home Assistant Auto Discovery configuration, please consider existing users.

Changes to entity IDs or MQTT topic structures can break existing dashboards and automations, so avoid changing them unnecessarily.

For new sensors, use sensible:

- Names
- Units
- Home Assistant device classes
- State classes
- Icons

when applicable.

## Documentation

Documentation lives in the `docs/` directory.

Documentation improvements are very welcome. This includes:

- Installation instructions
- Hardware and wiring information
- Configuration examples
- Troubleshooting
- Register documentation
- Home Assistant examples
- Notes about tested inverter models
- MQTT examples

Please use standard Markdown and keep documentation reasonably concise and easy to follow.

If instructions depend on a particular inverter model, firmware version, adapter, or software version, mention that explicitly.

## Pull Requests

A good pull request should include:

1. A short description of the problem or improvement.
2. An explanation of the changes made.
3. Details about how the changes were tested.
4. Your inverter model and relevant hardware details when the change involves Modbus communication or inverter behavior.
5. Screenshots, logs, MQTT payloads, or examples when they help explain the change.

Small pull requests are generally easier to review than large ones.

## Reporting Problems

If you find a bug, opening an issue before attempting a large fix can be helpful.

When reporting inverter communication problems, include relevant information such as:

- Inverter model
- Firmware version, if available
- RS485 adapter or gateway being used
- Relevant configuration
- Error messages or logs
- What you expected to happen
- What actually happened

Please remove passwords, credentials, public IP addresses, and other sensitive information before posting logs or configuration files.

## Code Style

There is currently no strict contribution style guide.

When modifying existing code:

- Follow the general style already used in the project.
- Prefer readable code over unnecessarily complex solutions.
- Use descriptive variable and function names.
- Add comments where behavior would otherwise be difficult to understand.
- Avoid adding dependencies unless they provide a clear benefit.

## License

By contributing to this repository, you agree that your contributions will be distributed under the same license as the project.

Thank you for helping improve **invt-modbus-mqtt**.
