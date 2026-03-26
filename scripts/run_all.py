#!/usr/bin/env python3
"""
Run full AMD_REE_Portal build: setup -> publish -> OGC -> map -> dashboard -> share.
Requires: ArcGIS Online org account, ARCGIS_PROFILE (optional), data files in data/.
"""
import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

def main():
    steps = [
        "01_project_setup.py",
        "02_publish_hosted_layers.py",
        "03_ogc_layers.py",
        "04_web_map.py",
        "05_dashboard.py",
        "06_share_and_download.py",
    ]
    for step in steps:
        path = SCRIPTS_DIR / step
        print(f"\n--- {step} ---")
        r = subprocess.run([sys.executable, str(path)], cwd=str(SCRIPTS_DIR))
        if r.returncode != 0:
            print(f"Step {step} exited with {r.returncode}")
            sys.exit(r.returncode)
    print("\nDone. See config/portal_state.json and docs/DELIVERABLES.md.")

if __name__ == "__main__":
    main()
