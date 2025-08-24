# Troubleshooting

- **No reaction from board**: verify 3V3/GND/SIG polarity and jumper.
- **UART transport fails**: check COM/tty path; try `device: auto`.
- **GPIO local fails**: ensure Linux, and `python3-gpiod` or `RPi.GPIO` installed.
