# Energy Analysis

The project documentation includes a first-order energy estimate for the prototype.

Representative documented loads include approximately 6 W for the drive motor, 5.5 W typical for steering, about 1 W for motor control, 0.40 W for the Arduino Uno and 0.63 W for the ESP32 in Wi-Fi operation.

The documented estimate gives a typical system power around 13.5 W, excluding the independently powered smartphone and ignoring conversion losses in the power banks.

## Engineering limitation

These figures are estimates based on typical operating values. Actual runtime depends on duty cycle, servo peaks, conversion efficiency, battery capacity at the relevant load and smartphone consumption.

The energy analysis therefore demonstrates system-level budgeting rather than a calibrated efficiency measurement.

## Future direction

A proposed extension is to use harvested solar energy directly for charging and to let live energy balance influence robot behavior. That would turn the light-seeking demonstration into a more explicit energy-autonomy experiment.
