#!/usr/bin/env python3
"""
Check ArcGIS credentials and portal URL. Run from project root with venv active:
  python scripts/check_credentials.py

Helps diagnose "Invalid username or password" when creds are correct in browser.
"""
import os
import sys
from pathlib import Path

# Load .env the same way as other scripts
sys.path.insert(0, str(Path(__file__).resolve().parent))
import env  # noqa: F401 - loads .env

def main():
    url = os.environ.get("ARCGIS_URL", "https://www.arcgis.com")
    username = os.environ.get("ARCGIS_USERNAME", "")
    password = os.environ.get("ARCGIS_PASSWORD", "")

    print("Using from .env / environment:")
    print(f"  ARCGIS_URL     = {url}")
    print(f"  ARCGIS_USERNAME= {username}")
    print(f"  ARCGIS_PASSWORD= [length={len(password)}] ends with: ...{repr(password[-3:]) if len(password) >= 3 else '(empty)'}")
    if not username or not password:
        print("\nMissing ARCGIS_USERNAME or ARCGIS_PASSWORD in .env. Add them and run again.")
        return 1

    from arcgis.gis import GIS
    try:
        gis = GIS(url, username, password)
        me = gis.users.me
        if me:
            print(f"\nOK: Logged in as {me.username}")
            return 0
        print("\nUnexpected: GIS connected but gis.users.me is None.")
        return 1
    except Exception as e:
        err = str(e).lower()
        print(f"\nLogin failed: {e}")
        if "invalid username or password" in err or "invalid username or password" in str(e):
            print("\nCommon causes when password is correct:")
            print("  1) Wrong portal URL. If you're in an ORGANIZATION:")
            print("     Set ARCGIS_URL to your org URL, e.g.:")
            print("     ARCGIS_URL=https://YOURORG.maps.arcgis.com")
            print("     (Find it: sign in at arcgis.com, look at the browser address bar or org settings.)")
            print("  2) Org uses SSO/SAML/OAuth only. Then username/password may be disabled.")
            print("     Use a token or run from ArcGIS Pro's Python (profile login) instead.")
            print("  3) Password contains # or !. In .env use quotes: ARCGIS_PASSWORD=\"YourPass!@#$\"")
        return 1

if __name__ == "__main__":
    sys.exit(main())
