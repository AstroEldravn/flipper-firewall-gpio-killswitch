# Testing Checklist

- [ ] Power‑on default state matches jumper.
- [ ] KILL ON asserts within <50 ms (UART RTS/DTR path).
- [ ] Relay coil protected (diode present, no excessive ringing).
- [ ] Host `dryrun` passes tests: `make test`.
