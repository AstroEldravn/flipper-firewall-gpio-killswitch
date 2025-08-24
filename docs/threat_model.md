# Threat Model

- **Attacker goal**: exfiltrate data or maintain a covert channel.
- **Defender response**: assert KILL to sever a physical link (power/USB/ETH).
- **Assumptions**:
  - Physical integrity of the kill board and cabling.
  - Trigger source is trusted or adequately authenticated.

**Mitigations**:
- Use **manual triggers** (reed, concealed switch) for PANIC.
- Keep **default‑safe** appropriate to your environment.
- Consider **tamper‑evident** enclosures.
