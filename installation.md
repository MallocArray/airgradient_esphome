# Installation

## Standard

* In ESPHome web interface, click New Device.  Give any name. Select any model of board, and click Skip on the final page to not install at this time. Click Edit on the new entry and replace with the contents of the .yaml file for your model.
* Alternatively, copy the .yaml file from the main folder for your model in this repo and place it in the `config` folder of your ESPHome.
* Make any desired changes to the substitutions to name the devices for your use case
* Install to the device using one of the ESPHome options.

> Note: by default ESPHome only syncs remote repositories that the packages are referencing once per day, so if changes are made to the repository, you may not get the updated config for up to 1 day after it is published.  You can remove the contents of the folder config/.esphome/packages to force it to update sooner

> Note: setting `add_mac_suffix: "true"` allows for multiple devices on your network at the same time and report as unique entries even if your `name:` field is duplicated, but it can cause ESPHome to not detect devices as Online after installing, since ESPHome is looking for only the `name:` field and the actual device name has the MAC address added to the end

> One way to resolve this is to change `add_mac_suffix: "false"` so the device name will match exactly.  If you have multiple devices, make sure to change the `name: `field to be unique for each device

> Another alternative is to add a static IP to the wifi configuration and configure ESPHome to ping the device by IP instead of hostname

> [Dashboard status light not working across subnets/zones · Issue #641 · esphome/issues (github.com)](https://github.com/esphome/issues/issues/641#issuecomment-534156628)

 Example for static IP

```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  manual_ip:
    static_ip: 192.168.1.121
    gateway: 192.168.1.1
    subnet: 255.255.255.0
    dns1: 192.168.1.1
```

## ESPHome Web install

Install a compiled file to your device all with just a browser and USB cable, no ESPHome install required.

Save the appropriate .bin file and go to [https://web.esphome.io/](https://web.esphome.io/) in your browser to connect your ESP device and send the .bin file to it

In some cases, the device may encounter errors using the web flash tool.  Steps to put the device in a special boot flash mode can be found here:
[https://forum.airgradient.com/t/airgradient-one-not-working-after-flashing-with-arduino/1326/4 ](https://forum.airgradient.com/t/airgradient-one-not-working-after-flashing-with-arduino/1326/4)

## Full YAML file

The `full_config` folder contains a single yaml file per model that contains the full standalone configuration, created by the `esphome config` command.  This adds in all of the optional parameters, so is much longer than the minimum configuration, but the single file contains all needed information to be completely independent from this repo.

Copy the full config file to your personal ESPhome config file and customize as desired, then install to your device.

## Troubleshooting

If some sensors are not showing valid readings after installing or upgrading, please remove the power cable from the device entirely for 5-10 seconds, then reconnect.  Many issues are resolved with a full power reset, as the software reset does not fully clear some situations.
