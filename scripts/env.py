"""
AMD_REE_Portal – shared connection and paths.

Authentication (aligned with ArcGIS API for Python docs):
- If ARCGIS_USERNAME and ARCGIS_PASSWORD are set in .env: use built-in login
  (GIS(url, username, password)) per API Reference Examples 2 & 3.
- Else: use stored profile (GIS(url, profile=...)). Create the profile once by
  running with username/password, or in Python:
  GIS(url, username=u, password=p, profile='home').

Note: The API doc does not list an 'interactive' parameter; browser login is
documented for OAuth (client_id). For SSO/OAuth-only orgs, use client_id or
create/save a profile after signing in elsewhere.

USGS_API_KEY is also loaded from .env but never committed.
"""
import os
from pathlib import Path

from arcgis.gis import GIS

# Workaround: arcgis.features.geo can fail to export _is_geoenabled (ImportError in geo/__init__.py),
# but other code (e.g. content.add) may still access geo._is_geoenabled. Provide a stub so it doesn't crash.
try:
    import arcgis.features.geo as _geo
    if not hasattr(_geo, "_is_geoenabled"):
        _geo._is_geoenabled = lambda df: False
except Exception:
    pass

# Optional: load .env from project root (no extra dependency; plain key=value)
# Values in .env: no comment stripping after # (we use first "=" only). Quote values with # or ! if needed.
_env_file = Path(__file__).resolve().parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            v = v.strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1].replace('\\"', '"')
            elif v.startswith("'") and v.endswith("'"):
                v = v[1:-1].replace("\\'", "'")
            if k.strip() and os.environ.get(k.strip()) is None:
                os.environ[k.strip()] = v

# ArcGIS connection
ARCGIS_PROFILE = os.environ.get("ARCGIS_PROFILE", "home")
ARCGIS_URL = os.environ.get("ARCGIS_URL", "https://www.arcgis.com")
ARCGIS_USERNAME = os.environ.get("ARCGIS_USERNAME", "").strip()
ARCGIS_PASSWORD = os.environ.get("ARCGIS_PASSWORD", "").strip()

# USGS Water Data API key (optional; enables higher rate limits for OGC API)
USGS_API_KEY = os.environ.get("USGS_API_KEY", "").strip() or None

# Project paths (repo root = parent of 'scripts')
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"

# Folder name in AGOL
PORTAL_FOLDER = "AMD_REE_Portal"

# Web map and dashboard names
WEB_MAP_TITLE = "AMD_REE_InteractiveMap"
DASHBOARD_TITLE = "AMD & REE Live Mapping Dashboard"


def get_gis() -> GIS:
    """
    Centralized GIS factory per ArcGIS API for Python.

    - If ARCGIS_USERNAME and ARCGIS_PASSWORD are set: use built-in login
      (documented in API Reference as username/password).
    - Else: use stored profile (profile must already exist; create it once
      with username/password + profile= name).
    """
    url = ARCGIS_URL or "https://www.arcgis.com"
    if ARCGIS_USERNAME and ARCGIS_PASSWORD:
        # Documented built-in login (API Reference Examples 2 & 3)
        gis = GIS(url, username=ARCGIS_USERNAME, password=ARCGIS_PASSWORD)
    else:
        # Use stored profile (no 'interactive' – not in API constructor docs)
        gis = GIS(url, profile=ARCGIS_PROFILE)
    if gis.users.me is None:
        raise RuntimeError(
            "ArcGIS connection is not authenticated (gis.users.me is None). "
            "Check: (1) ARCGIS_URL – use org URL if needed, e.g. https://yourorg.maps.arcgis.com; "
            "(2) ARCGIS_USERNAME and ARCGIS_PASSWORD in .env; "
            "(3) If your org uses SSO/OAuth only, create a profile once with credentials or use client_id."
        )
    return gis

