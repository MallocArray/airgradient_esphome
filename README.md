# AirGradient ESPHome Configurations

ESPHome yaml files for AirGradient devices to maintain the research and accuracy of AirGradient sensors, while also gaining the benefits of ESPHome/HomeAssistant for easy to use switches, buttons, configurations, and dashboards.  Maintains the ability to also send data to the AirGradient Dashboard, which can also be disabled/removed to keep all data local.

<img src="image/README/1715467068556.png" width=25% height=25%>

## [Installation](/installation.md)

## [Configuration](/configuration.md)

## [Calibration](/calibration.md)

## [Packages](/packages.md)

List of available packages to customize your device and gain additional features

## Breaking Changes

* 5.0.0 is a major version upgrade as switching to esp-idf is not fully supported via OTA. Highly recommend doing one USB flash of 5.0.0 and later to the AirGradient ONE and OpenAir devices to reformat the storage to support esp-idf.  Future updates can be done Over-The-Air without issue.
  * If not done, the device is likely to reboot at some point and switch to the standby partition, returning to a version prior to 5.0.0
  * [Seeing an Old Firmware Version After Update? Here&#39;s Why &amp; How to Fix It · Issue #1821 · Blackymas/NSPanel_HA_Blueprint](https://github.com/Blackymas/NSPanel_HA_Blueprint/issues/1821)
  * [Read/Write bootloader, partition table and any partition via OTA by angelnu · Pull Request #5535 · esphome/esphome](https://github.com/esphome/esphome/pull/5535)

## Changes

* Added optional substitutions to implement batch-specific PM2.5 corrections using values provided by AirGradient
  [See details in the packages.md file under the PMS5003 section.](packages.md#sensor_pms5003yaml)
* Restored logging to default values as it no longer repeats messages about components taking too long to complete

## Features

Many added features can be found in HomeAssistant by going to Settings>Devices and selecting the AirGradient device.  Alternatively, add `web_server:` to the config file to enable a built-in web server on the AirGradient device (Not recommended for devices based on the D1 Mini ESP8266)

- Compact single page display by default with all relevant sensor readings
- Display Contrast slider to dim the display
- Enable different pages of information to be shown on the OLED display, or leave the default of a single page with all relevant information

  ![1703765819874](image/README/1703765819874.png)
- Button to initiate a SenseAir S8 CO2 Calibration on demand

  ![1703765340274](image/README/1703765340274.png)
- Switch to enable or disable SenseAir S8 CO2 sensor Automatic Baseline Calibration (ABC)

  ![1704131891282](image/README/1704131891282.png)
- Button to view the current S8 ABC interval (confirm if ABC is disabled or enable, which defaults to every 7 days) View ESPHome logs to see the output of this button

  ![1703765530959](image/README/1703765530959.png)
- Switch to disable LED output on AirGradient ONE model
- Brightness slider to adjust intensity of AirGradient ONE LED

  ![1703765585475](image/README/1703765585475.png)
- Switch to toggle display between Fahrenheit and Celsius and persist between reboots

  ![1703765618154](image/README/1703765618154.png)
- Switch to enable or disable uploading to AirGradient Dashboard via API (Choose to keep data local or also send to AirGradient)

  ![1703765631637](image/README/1703765631637.png)
- Utilize hardware configuration buttons on AirGradient Pro v3.7 and higher

  - Short press (Less than 1 second) - Toggle between F and C on display
  - Long press (More than 1 second, less than 5) - Trigger manual CO2 calibration
- Leverage automation in HomeAssistant to turn on the "Blank" page and turn off all other pages to effectively disable the display output.  Could also turn off the LED strip or set Brightness to 0 to eliminate output while still collecting sensor data

## Support me

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O5O31C8PHG)

[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mallocarray)

## Todo list

More features are planned to be added to this repo

- [ ] Deprecate Extended Life packages and use a substitution to allow for adjusting update_interval
