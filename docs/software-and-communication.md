# Software & Communication

The repository contains several software targets:

- Arduino drive/control firmware,
- ESP32 coordination and networking firmware,
- Android “Sunseeker” application,
- development and documentation tools.

## Distributed control

The Android image-processing module detects light sources and sends derived control information. The ESP32 acts as the networked coordination layer and communicates with the Arduino responsible for the physical drive system.

This separation reflects a central Systems Engineering challenge: each subsystem can work individually while the complete behavior depends on correctly defined interfaces and timing.

## Repository structure

Executable sources are kept under `src/`. The repository also contains the original project documentation, drawings and presentation material.

The GitBook provides a concise system-level view; the original repository remains the detailed engineering record.
