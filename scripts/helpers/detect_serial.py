import sys, glob, platform

def list_ports():
    system = platform.system().lower()
    candidates = []
    if system == "windows":
        # Typical COM ports up to COM256
        candidates = [f"COM{i}" for i in range(1, 257)]
    elif system == "darwin":
        candidates = glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*")
    else:
        candidates = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*") + glob.glob("/dev/tty.*")

    found = []
    for c in candidates:
        try:
            with open(c, "rb", buffering=0):
                pass
            found.append(c)
        except Exception:
            pass
    return sorted(set(found))

if __name__ == "__main__":
    for p in list_ports():
        print(p)
