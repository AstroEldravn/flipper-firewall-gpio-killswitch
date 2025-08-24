# Firmware‑Agnostic Control

We never call firmware APIs. The board expects only **SIG = HIGH/LOW (3.3 V)**.

## Wiring patterns

1. **Flipper Zero → SIG**
   - Use 3V3, GND, and a GPIO (e.g., PC3/D7). Set pin `HIGH` to kill.
2. **Reed switch / Button**
   - Pull‑up SIG to 3V3; switch to GND for active‑low (or invert via jumper).
3. **USB‑UART → transistor gate**
   - Drive SIG via RTS/DTR using `uart_serial` transport.

## Safe defaults

- **Jumper** selects:
  - *Allow by default* (SIG HIGH → kill).
  - *Kill by default* (SIG LOW → allow).

See `docs/wiring/safety_notes.md`.
