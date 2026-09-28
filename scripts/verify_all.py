#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
root = Path(__file__).resolve().parents[1]
checks = [
    root / '01_POWER_Handover/01_03_POWER_Verification_Script.py',
    root / '02_ESP32_USB_Handover/02_03_ESP32_USB_Verification.py',
]
for check in checks:
    code = subprocess.call([sys.executable, str(check)], cwd=root)
    if code:
        raise SystemExit(code)
