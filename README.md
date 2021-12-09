# airgradient_esphome
ESPHome definition for an AirGradient DIY device to send data to HomeAssistant and AirGradient servers while maintaining a similar functionality and look to the official AirGradient Arduino IDE sketch

At this time the ChipID needed for adding to the AirGradient website is not displayed.  May need to use Arduino sketch to get this ID then use ESPHome

## Configuration
If all original sensors (PMS5003, Senseair S8, SHT3x) are connected, airgradient.yml should be fully ready
If some sensors are not installed, comment or remove the associated sections in sensor: and display: and http_request.post:
Commented code supports TVOC readings from SGP30 sensor, but in testing, it required being connected to 3.3v instead of 5v as wired on the AirGradient board.  Also does not appear to work if the OLED display is connected, but works if display is physically removed.

To add your wifi SSID and password, either remove the "!secret" section and type in your information, or edit the secrets.yaml file with
your information so it is not hard coded into the device's file.

## Fonts
You may substitute any font as desired.  Included font "Liberation Sans" is open source and very similar to Arial that is
used by the official AirGradient Arduino sketch
