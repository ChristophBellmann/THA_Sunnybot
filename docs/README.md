# Sunnybot: Die Motte

A Systems Engineering student project in which an autonomous mobile robot searches for the strongest available light source.

The project was developed as a team project at Hochschule Augsburg. The assignment was to build a deliberately “useless machine” while applying multiple engineering disciplines. The result combines mechanics, electronics, embedded control, networking, image processing and an Android user interface.

## The idea

“Die Motte” (“The Moth”) tries to remain “happy” by continuously seeking light. Solar-cell measurements provide directional information, while a smartphone camera and image-processing software can refine the direction toward a light source. An ESP32 coordinates networked information and an Arduino controls the drive system.

The concept turns a playful assignment into a distributed mechatronic system with real interfaces between sensing, perception, communication and actuation.

## Project attribution

**Team Sunnybot**
- Christian Gross — mechanical construction, drive control, networking and motion control
- Christoph Bellmann — Git environment, software architecture, Android app and image-processing-based control information
- Felix Schirmer — solar-cell modules, image-processing algorithms and energy analysis

This documentation presents the project as a university team project. It is included in Christoph Bellmann’s engineering portfolio because it demonstrates his contributions to the system and its integration; it is not presented as a solely developed Renewable Energy Design product.

Continue with [System Concept](system-concept.md), [Architecture](architecture.md), [Light Seeking](light-seeking.md), [Software & Communication](software-and-communication.md), [Energy Analysis](energy-analysis.md), and [Development & Outlook](development-and-outlook.md).
