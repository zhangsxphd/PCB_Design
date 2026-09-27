#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
root = Path(__file__).resolve().parents[1]
cmd = [sys.executable, str(root/'01_POWER_Handover/01_03_POWER_Verification_Script.py')]
raise SystemExit(subprocess.call(cmd, cwd=root))
