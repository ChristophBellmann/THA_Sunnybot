# Architecture

Sunnybot is a distributed mechatronic system rather than a single-controller robot.

## Main subsystems

- **Solar-cell sensing** measures local light intensity and provides directional information.
- **Android smartphone** uses camera images for light-source detection and direction estimation.
- **ESP32** handles network communication and higher-level coordination.
- **Arduino Uno** controls steering and drive hardware.
- **Drive platform** provides propulsion and steering.
- **User interaction** changes the light environment and therefore the robot’s behavior.

## Hardware documented in the project

The prototype uses two 28BYJ-48 12 V motors, A4988 motor drivers, an MG996R-class steering servo, Arduino Uno, ESP32 and separate power banks for the drive and control electronics.

The mechanical platform uses acrylic plates, printed mounts and a combination of driven, steering and support wheels.

The architecture intentionally distributes responsibilities so that sensing, perception and actuation can be developed and tested as separate modules.
