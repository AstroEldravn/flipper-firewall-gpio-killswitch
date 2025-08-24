# Killswitch Host API

## Config (YAML)

```yaml
transport:
  type: uart_serial           # uart_serial | gpio_local | dryrun
  device: auto                # auto or explicit path (e.g., /dev/ttyUSB0, COM5)
  line: rts                   # rts | dtr (uart_serial)
  invert_logic: false

policy:
  default_kill_state: false   # false=allow; true=kill
  debounce_ms: 100
  triggers:
    - name: panic_file
      type: file_exists
      path: /tmp/KILL_NOW
      action: kill_on
    - name: fw_log
      type: log_regex
      path: /var/log/ufw.log
      regex: "BLOCK.*203.0.113.66"
      action: kill_on
    - name: clear_after_10s
      type: timer
      seconds: 10
      action: kill_off

alerts:
  - type: log_only
  - type: desktop_notify
  - type: webhook
    url: http://localhost:8080/hook
  - type: syslog
```

## Actions
- `kill_on`  → set_kill(True)
- `kill_off` → set_kill(False)
