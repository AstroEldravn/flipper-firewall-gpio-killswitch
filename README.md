# Flipper Firewall GPIO Killswitch

![Status](https://img.shields.io/badge/status-alpha-success)
![License](https://img.shields.io/badge/license-MIT-informational)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

A **hardware‑first**, **firmware‑agnostic** killswitch you can toggle from *anything* that outputs **3.3 V HIGH** — works great with **Flipper Zero** no matter which firmware you run.  
Use it to cut **power**, **USB data**, or an **Ethernet pair** in panic or policy‑driven scenarios.

DISCLAIMER: Yo, I'm not responsible if you destroy some shit by accident. Have fun and be careful. Test this on equipment that's deprecated or no longer useful. Not to be used maliciously.

> TL;DR — Wire 3V3/GND/SIG to our little board. Flip a GPIO (from Flipper, reed switch, USB‑UART, or Raspberry Pi) and the target link dies.

---

## ✨ Highlights

- **Firmware‑agnostic:** Only needs a pin state (HIGH/LOW), not SDKs.
- **Safe defaults:** Select default‑safe state (kill by default or allow by default) via jumper.
- **Host rules engine:** Optional Python app maps triggers → GPIO action.
- **Multiple transports:** `uart_serial`, `gpio_local` (Linux), or `dryrun` for tests.
- **Pluggable alerts:** Log, desktop notification, webhook, and syslog.

---

## 🔌 Topology (at a glance)

```mermaid
flowchart LR
  subgraph Host["Host (optional)"]
    A[Rules Engine<br/>Python] -->|set_kill(True/False)| T
  end
  subgraph Trigger
    FZ[Flipper Zero<br/>any firmware]:::fz --- T[3.3V SIG]
    RS[Reed Switch / Button] --- T
    UART[USB-UART<br/>RTS/DTR] --- T
  end
  subgraph Board["Killswitch Board"]
    T --> D[Driver (NPN+MOSFET or Relay)]
    D --> CUT[(Cut Power / USB D+ D- / ETH Pair)]
  end
  classDef fz fill:#ff7,stroke:#333,stroke-width:1px;
```

---

## 🧰 What’s in the box

- **`hardware/`** – Reference circuits (MOSFET latch, DPDT relay for USB, relay for Ethernet).
- **`host/`** – Python rules engine + transports (UART, local GPIO).
- **`flipper/`** – Optional helpers that work with any firmware (simple pin toggle).
- **`docs/`** – Wiring, firmware‑agnostic control, threat model, troubleshooting.
- **`targets/`** – Ready‑to‑build reference targets with wiring instructions.

---

## 🚀 Quickstart (Demo without hardware)

```bash
# 1) Install deps
make setup

# 2) Run the demo: toggles a DryRun driver based on a file trigger
make run
# Touch /tmp/KILL_NOW to assert the "kill"; remove it to clear
```

You should see logs like:
```
[info] transport=dryrun state=True
[info] trigger=panic_file matched → KILL ON
```

---

## 🔧 Quickstart (with USB‑UART → transistor gate)

1. Build the **USB data cut** or **power cut** target (see `targets/`).
2. Wire **3V3**, **GND**, **SIG** from your USB‑UART + driver to the board.
3. Configure:
   ```yaml
   # host/config/example.yaml
   transport:
     type: uart_serial
     device: auto        # or /dev/ttyUSB0, COM5
     line: rts           # rts | dtr
     invert_logic: false
   ```
4. Run it:
   ```bash
   make run
   ```

---

## 🧪 Policy Triggers (examples)

- **`file_exists`**: assert kill while a file exists (panic key).
- **`timer`**: auto‑clear kill after N seconds.
- **`log_regex`**: tail a log and match a regex (e.g., firewall log).
- **`http_probe`**: periodically fetch a URL and match a status code or text.

See complete schema in [`docs/api/killswitch_api.md`](docs/api/killswitch_api.md).

---

## 🛠️ Flipper Zero Pinout (quick ref)

```text
  [3V3]  [GND]  [PC3/D7]  [PC1/D9] ...
    |      |       \——> Suggested SIG pin
```

> Any **3.3 V‑tolerant GPIO** is fine. No SDK required; set pin HIGH to kill (or LOW if inverted).

---

## 🧯 Safety

- Use flyback diodes with inductive loads (relays).
- Keep USB D+/D− trace lengths symmetric.
- Default‑safe jumper lets you choose fail‑open or fail‑closed.

See `docs/wiring/safety_notes.md`.

---

## 🧩 Roadmap

- GPIO expander transport (MCP23017 over I²C).
- BLE transport via generic GATT GPIO service.
- Optional OLED status panel.

---

## 📜 License

MIT — see `LICENSE`.
