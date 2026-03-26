#!/usr/bin/env python3
"""
Step 3: Add USGS OGC API – Features layers to ArcGIS Online.
Uses 'Add Item > From URL' with OGC API Features URL. Sets refresh interval
and popup info where supported via item metadata/description.
"""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, PORTAL_FOLDER, USGS_API_KEY, get_gis

ENDPOINTS_CONFIG = CONFIG_DIR / "usgs_ogc_endpoints.json"


def _get_folder(gis, folder_id):
    """Return Folder object for portal folder or root."""
    if folder_id:
        return gis.content.folders.get(folder=PORTAL_FOLDER)
    return gis.content.folders.get()


def _url_with_api_key(url, api_key):
    """Append USGS api_key to URL for higher rate limits; key is not stored in repo."""
    if not api_key or "api_key=" in url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}api_key={api_key}"

def add_ogc_item(gis, url, title, description, folder_id, snippet=None):
    """
    Add OGC API - Features layer as an item in AGOL.
    Type for OGC API Features in AGOL is typically added via URL;
    the Python API accepts item_type and url for add().
    """
    item_props = {
        "type": "OGC Feature Service",
        "typeKeywords": "OGC,Feature Service,Feature Layer",
        "title": title,
        "description": description or "",
        "tags": "USGS, water data, OGC API, Features, live",
    }
    if snippet:
        item_props["snippet"] = snippet
    if folder_id:
        item_props["folder"] = folder_id

    # Append USGS API key from env if set (higher rate limits; key lives in env/.env, not repo)
    url = _url_with_api_key(url, USGS_API_KEY)
    folder = _get_folder(gis, folder_id)
    try:
        from arcgis.gis import ItemProperties
        props = ItemProperties(title=title, item_type="OGC Feature Service", tags="USGS, water data, OGC API, Features, live", snippet=snippet or title, description=description or "")
    except (ImportError, TypeError):
        props = item_props
    add_result = folder.add(props, url=url)
    item = add_result.result() if hasattr(add_result, "result") else add_result
    return item

def _build_items_url(col, base_url):
    """Build OGC API – Features items URL for ArcGIS Online (must return GeoJSON)."""
    url = col.get("url")
    if not url:
        items_path = col.get("items_path", "/items")
        url = f"{base_url.rstrip('/')}/collections/{col['id']}{items_path}"
    params = col.get("query_params") or {}
    if params:
        q = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{q}" if "?" not in url else f"{url}&{q}"
    return url

def main():
    gis = get_gis()
    cfg = json.loads(ENDPOINTS_CONFIG.read_text())
    base_url = cfg.get("base_url", "https://api.waterdata.usgs.gov/ogcapi/v0")
    state_path = CONFIG_DIR / "portal_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    folder_id = state.get("folder_id")

    added = {}
    for col in cfg.get("collections", []):
        url = _build_items_url(col, base_url)
        title = col.get("title", col["id"])
        desc = col.get("description", "")
        refresh = col.get("refresh_minutes", 60)
        popup = col.get("popup_fields", [])
        desc += f"\n\nRefresh: every {refresh} min. Popup fields: {', '.join(popup)}."
        try:
            item = add_ogc_item(gis, url, title, desc, folder_id, snippet=f"USGS {title}")
            added[col["id"]] = {"item_id": item.id, "url": item.url or url}
            print(f"Added OGC layer: {col['id']} -> {item.id}")
        except Exception as e:
            print(f"Failed to add {col['id']}: {e}")

    state["ogc_layers"] = added
    state_path.write_text(json.dumps(state, indent=2))
    return state

if __name__ == "__main__":
    main()
