# Overview

The GPIO Killswitch is a tiny board + optional host app that lets you **physically sever** a connection (power, USB data, or an Ethernet pair) based on a simple **3.3 V logic signal**. The signal can come from a Flipper Zero, reed switch, button, USB‑UART, or a Linux SBC GPIO.

- **No firmware coupling**: it only watches a pin level.
- **Host optional**: A Python rules engine is provided but not required.
- **Default‑safe**: jumper chooses fail‑open or fail‑closed behavior.
