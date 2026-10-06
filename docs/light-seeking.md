# Light Seeking

The robot combines two different sources of information about light.

## Solar-cell sensing

Solar-cell voltage measurements provide a direct indication of illumination and can be used to determine a promising search direction.

## Camera-based perception

The Android smartphone uses its cameras and image processing to identify strong light sources and derive steering information.

## Combined behavior

In the documented control sequence, solar-cell measurements can initiate a new orientation process. Camera-based processing then supplies more detailed light-source information. The ESP32 coordinates this information and forwards motion commands to the Arduino drive controller.

This creates a simple sensor-fusion concept: coarse physical light sensing and image-based directional perception contribute to the same behavioral goal.

## Interaction

Covering a light source or illuminating the robot directly changes its sensed environment. The robot then reorients or moves toward the newly dominant source, making the control system visible and interactive.
