from host.config_loader import load_config, Config

def test_load_example():
    cfg = load_config("host/config/example.yaml")
    assert isinstance(cfg, Config)
    assert cfg.transport.type in ("dryrun", "uart_serial", "gpio_local")
