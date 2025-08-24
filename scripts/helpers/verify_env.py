import importlib, sys

mods = ["yaml", "pydantic", "serial", "requests"]
ok = True
for m in mods:
    try:
        importlib.import_module(m)
        print(f"[OK] {m}")
    except Exception as e:
        print(f"[MISSING] {m} ({e})")
        ok = False

if not ok:
    sys.exit(1)
