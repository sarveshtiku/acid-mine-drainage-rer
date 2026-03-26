#!/usr/bin/env python3
"""
Step 6: Public sharing and data download.
- Share Web Map and Dashboard with everyone (public).
- Ensure each hosted feature layer has Export Data enabled and is shared.
- Optionally add download link in dashboard (documented in README).
"""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, get_gis


def main():
    gis = get_gis()
    state_path = CONFIG_DIR / "portal_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}

    # Share with everyone (public)
    to_share = []
    if state.get("web_map_id"):
        to_share.append(state["web_map_id"])
    if state.get("dashboard_id"):
        to_share.append(state["dashboard_id"])
    for layer_key, item_id in state.get("hosted_layers", {}).items():
        to_share.append(item_id)
    for ogc_id, info in state.get("ogc_layers", {}).items():
        to_share.append(info["item_id"])

    for item_id in to_share:
        try:
            item = gis.content.get(item_id)
            if item and not item.shared_with["everyone"]:
                item.share(everyone=True)
                print(f"Shared: {item.title}")
            elif item:
                print(f"Already shared: {item.title}")
        except Exception as e:
            print(f"Share failed {item_id}: {e}")

    # Hosted layers: ensure Extract/Export is enabled (done in 02; re-assert if needed)
    for layer_key, item_id in state.get("hosted_layers", {}).items():
        try:
            item = gis.content.get(item_id)
            if item and item.layers:
                fl = item.layers[0]
                if hasattr(fl, "manager") and hasattr(fl.manager, "update_definition"):
                    fl.manager.update_definition({"capabilities": "Query,Extract"})
        except Exception:
            pass

    print("Sharing and export settings applied.")
    return state

if __name__ == "__main__":
    main()
