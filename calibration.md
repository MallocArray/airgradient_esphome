# Calibration

Many of the official calibration algorithms from AirGradient are also implemented in this repository.
https://www.airgradient.com/documentation/calibration-algorithms/

## EPA PM2.5 Calibration

This algorithm is applied by default to all PMS5003(t) sensors in this repository.  If it is desired to not apply this and instead use raw values from the sensors, replace the package file with the one ending with `_uncorrected.yaml`

## Batch Specific PM2.5 Calibration

AirGradient detected that PMS5003 sensors after 2023-10-30 used a different manufacturer calibration that results in lower PM2.5 values under low concentrations.  AirGradient has developed an algorithm and tested values to correct these values when they are less than 31 ug/m3

In this repo, 2 substitution values can be adjusted to apply the calibration. In the main YAML file for the device, add a substitutions item and the follow parameters if not already present.

```yaml
substitutions:
  pm_2_5_scaling_factor: '1'
  pm_2_5_intercept: '0'
```

Adjust the scaling factor and intercept specific to your requirements.  The values from AirGradient can be found in the AirGradient Dashboard site under Hardware>Advanced Settings>PM 2.5

Under "Special formulas by specific batch" select a batch that matches the label on the sensor inside of your AirGradient, and take note of the `Scaling Factor` and `Offset` values to copy to the ESPHome YAML file.

Refer to the AirGradient page for the most current values, and they are planning on adding device specific formulas in the future
https://app.airgradient.com/settings/hardware

| Batch ID            | Scaling Factor   | Offset |
|---------------------|------------------|--------|
| PMS5003_20231030    | 0.02838          | 0      |
| PMS5003_20231218    | 0.03525          | 0      |
| PMS5003_20240104    | 0.02896          | 0      |
| PMS5003_20240826    | 0.03863          | 0      |
| PMS5003_20250116    | 0.02983          | 0      |

https://www.airgradient.com/blog/update-on-pms5003-calibration/

## Temperature and Humidity Calibration for Open Air Outdoor monitors

The algorithm from AirGradient for the PMS5003T sensors used in the Open Air for both Temperature and Humidity are applied by default. If it is desired to not apply this and instead use raw values from the sensors, replace the package file with the one ending with `_uncorrected.yaml`
