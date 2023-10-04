# AirGradient ESPHome Configurations

ESPHome yaml files for an AirGradient DIY devices to send data to HomeAssistant and AirGradient servers while maintaining a similar functionality and look to the official AirGradient Arduino IDE sketch

## Configuration

If all original sensors (PMS5003, Senseair S8, SHT3x) are connected, airgradient-basic.yml should be fully ready
If some sensors are not installed, comment or remove the associated sections in sensor: and display: and http_request.post:
Code supports TVOC readings from SGP30 sensor, but in testing, when used with the Basic board, it required being connected to 3.3v instead of 5v as wired on the AirGradient board.  Also does not appear to work if the OLED display is connected, but works if display is physically removed.

To add your wifi SSID and password, either remove the "!secret" section and type in your information, or edit the secrets.yaml file with
your information so it is not hard coded into the device's file.

## Installation

Copy the .yaml files and any associated fonts or secrets.yaml files to the config folder in your ESPHome installation.

Alternatively, save the .bin file and go to [https://web.esphome.io/](https://web.esphome.io/) in your browser to connect your ESP device and sent the .bin file to it, without having ESPHome installed

## Fonts

You may substitute any font as desired.  Included font "Liberation Sans" is open source and very similar to Arial that is
used by the official AirGradient Arduino sketch

Future configurations will begin using fonts downloaded directly from Google's servers so they will not need to be present in the same folder as the .yaml files
