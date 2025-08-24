# MOSFET Low-Side Latch (Reference)

```mermaid
flowchart LR
  SIG -->|via NPN| MOSFET[AO3400A Gate]
  MOSFET --> LOAD[Load / Coil]
  LOAD --> GND
  VCC --> LOAD
  DIODE[[Flyback Diode]] --> across LOAD
```
