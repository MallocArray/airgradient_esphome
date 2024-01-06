# AirGradient ESPHome Configurations

ESPHome yaml files for AirGradient devices to maintain the research and accuracy of AirGradient sensors, while also gaining the benefits of ESPHome/HomeAssistant for easy to use switches, buttons, configurations, and dashboards.  Maintains the ability to also send data to the AirGradient Dashboard, which can also be disabled/removed to keep all data local.

## Breaking Changes

In the 1.x release of these configurations, some breaking changes are introduced

* The devicename has been shortened from "airgradient-*" to "ag-".  This matches the Friendly Name convention and results in a shorter overall devicename.  You may keep yours at the longer full name if desired, but for the Open Air, the name became longer than allowed
* Substitution entry for "friendly_devicename" has been renamed to "friendly_devicename" to better match it's use case instead of the legacy use
* The name of the CO2 sensor has been changed to just "CO2" from the previous "Senseair S8 CO2" to shorten overall sensor name length and match other sensors that are named for what they are measuring and not the name of the sensor itself.  This will result in a new sensor registered to your device in HomeAssistant and the previous one will be "Unavailable".  You may need to update any graphs or other dashboard entries with the new CO2 entry
* New switch added to enable/disable Automatic Background Calibration of the Senseair S8 CO2 sensor.  If previously disabled, on the first install of the 1.x config, it will be enabled again.  Disable after installation if desired.

## Features

Many added features can be found in HomeAssistant by going to Settings>Devices and selecting the AirGradient device.  Alternatively, add `web_server:` to the config file to enable a built-in web server on the AirGradient device (No recommended for devices based on the D1 Mini ESP8266)

- Compact single page display by default with all relevant sensor readings
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
- Leverage automations in HomeAssistant to turn on the "Blank" page and turn off all other pages to effectively disable the display output.  Could also turn off the LED strip or set Brightness to 0 to eliminate output while still collecting sensor data

## Installation

### Standard

Copy the .yaml file from the main folder for your model and place it in the `config` folder of your ESPHome.  Make any desired changes to the substitutions to name the devices for your use case

> Note: by default ESPHome only syncs remote repositories that the packages are referencing once per day, so if changes are made to the repository, you may not get the updated config for up to 1 day after it is published.  You can remove the contents of the folder config/.esphome/packages to force it to update sooner

> Note: setting `add_mac_suffix: "true"` allows for multiple devices on your network at the same time and report as unique entries, but it can cause ESPHome to not detect devices as Online after installing, since ESPHome is looking for only the `devicename:` field and the actual device name has the MAC address added to the end.
>
>     One way to resolve this is to change`add_mac_suffix: "false"` so the devicename will match exactly.  If you have multiple devices, make sure to change the `devicename: `field to be unique for each device
>
>     Another alternative is to add a static IP to the wifi configuration and configure ESPHome to ping the device by IP instead of hostname
>
> [Dashboard status light not working across subnets/zones · Issue #641 · esphome/issues (github.com)](https://github.com/esphome/issues/issues/641#issuecomment-534156628)
>
> Example for static IP
>
> ```yaml
> wifi:
>   ssid: !secret wifi_ssid
>   password: !secret wifi_password
>   manual_ip:
>     static_ip: 192.168.1.121
>     gateway: 192.168.1.1
>     subnet: 255.255.255.0
>     dns1: 192.168.1.1
> ```

#### Using local packages

By default, packages are referencing this GitHub repository, allowing you to do a new Install from ESPHome dashboard to get the latest modifications without downloading other files, but does require an Internet connection.  If you wish to have more control over modifications or only reference local files, copy the `packages` folder to your local ESPHome folder and replace `github://MallocArray/airgradient_esphome/packages` with `!include packages`

> Example: `board: github://MallocArray/airgradient_esphome/packages/sensor_s8.yaml` becomes `board: !include packages/sensor_s8.yaml`

### ESPHome Web install

Install a compiled file to your device all with just a browser and USB cable, no ESPHome install required.

Save the appropriate .bin file and go to [https://web.esphome.io/](https://web.esphome.io/) in your browser to connect your ESP device and send the .bin file to it

> In some cases, the device may encounter errors using the web flash tool.  Steps to put the device in a special boot flash mode can be found here:
> https://forum.airgradient.com/t/airgradient-one-not-working-after-flashing-with-arduino/1326/4

### Full YAML file

Configuration files reference other packages files, making for a very modular configuration, but requires looking at multiple files to see the entire picture.

The `full_config` folder contains a single yaml file per model that contains the full standalone configuration, created by the `esphome config` command.  This adds in all of the optional parameters, so is much longer than the minimum configuration, but the single file contains all needed information to be completely independent from this repo.

Copy the full config file to your personal ESPhome config file and customize as desired, then install to your device.

## Configuration

If all original sensors (PMS5003, Senseair S8, SHT4x) are connected, configuration files should be ready
If some sensors are not installed, comment or remove the associated sections under `packages:`

The PMS5003 sensor by default collects readings every second.  Since this device has a limited lifespan, it is possible to extend the life by collecting readings less frequently, although this could impact the accuracy of the readings collected, since there will not be constant airflow through the device when the fan shuts down.  To collect readings every 2 minutes, change the line for the pms5003 sensor to `pm_2.5: !include packages/sensor_pms5003_extended_life.yaml`

> See [PMSX003 Particulate Matter Sensor — ESPHome](https://esphome.io/components/sensor/pmsx003.html#sensor-longevity) for more information

To add your WiFi SSID and password, add your SSID and password information, per ESPHome specifications

```yaml
wifi:
  ssid: NachoWiFi
  password: 123456123456
```

To modify other components, download the modify the associated packages file and modify as desired and update the packages reference to use the !include method mentioned in the Installation section. You may also use the [Extend](https://esphome.io/guides/configuration-types.html#extend) option to make minor modifications without editing the packages file.

Several packages are available in the `packages` folder that can be added or removed as needed.  For example, the display package includes configuration for multiple pages of information that can be enabled or disabled, or you may wish to change to the package that has a single page to avoid extra switches in HomeAssistant or if you know you won't be using the other pages and want to save on flash memory space.

## Additional Information

MQTT support has been mentioned in the AirGradient forums several times.  ESPHome supports this by adding a few lines to the main yaml file. Add the relevant information for your configuration. Read more about it here:
[https://esphome.io/components/mqtt.html](https://esphome.io/components/mqtt.html)

## Todo list

Several more features are planned to be added to this repo

- [ ] Support for Open Air without CO2 sensor
- [ ] Explore options for disabling display/LED during certain times (May be differed to HomeAssistant Automations)
- [ ] Standardize font on AirGradient Basic display to match Pro
- [ ] Reduce number of fonts used in the multi_page package
  - [ ] Open Sans displays a consistent height, but some characters, such as F and 0 are mismatched, the left side is double line thick while right is single line
  - [ ] Poppins Light is consistent thickness, but numbers are taller than letters, giving a mismatched height
- [ ] Add GitHub actions to automatically build updated .bin files as needed

* [ ] Add support for esp32_improv and improv_serial
  * [ ] [https://esphome.io/guides/creators.html](https://esphome.io/guides/creators.html "https://esphome.io/guides/creators.html")
* [ ] Add support for dashboard_import and project information
  * [ ] [https://esphome.io/guides/creators.html](https://esphome.io/guides/creators.html "https://esphome.io/guides/creators.html")
