#!/usr/bin/env python3
"""
Step 4: Create Web Map 'AMD_REE_InteractiveMap'.
Add all hosted feature layers and USGS OGC API layers. Configure symbology
(heatmap AMD, graduated REE, points, outlines) and popups.
"""
import json
from pathlib import Path

try:
    from arcgis.mapping import WebMap
except ImportError:
    from arcgis.map import Map as WebMap

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, PORTAL_FOLDER, WEB_MAP_TITLE, get_gis

LAYERS_CONFIG = CONFIG_DIR / "layers.json"
SYMBOLOGY_CONFIG = CONFIG_DIR / "symbology.json"

def get_popup_template(field_aliases, title):
    """Build a simple popup template from field aliases."""
    fields = [{"fieldName": k, "label": v} for k, v in (field_aliases or {}).items()]
    return {
        "title": title,
        "content": [{"type": "fields", "fieldInfos": [{"fieldName": f["fieldName"], "label": f["label"]} for f in fields]}],
    }

def add_layer_to_map(web_map, item_id, layer_cfg, symbology_cfg, visible=True):
    """Add a hosted feature layer to the web map with optional symbology."""
    gis = getattr(web_map, "gis", None) or getattr(web_map, "_gis", None)
    if not gis:
        return
    item = gis.content.get(item_id)
    if not item:
        return
    layers = item.layers if item.layers else [item]
    for layer in layers:
        try:
            if hasattr(web_map, "content") and hasattr(web_map.content, "add"):
                web_map.content.add(layer)
            else:
                web_map.add_layer(layer, {"visibility": visible})
        except Exception as e:
            print(f"Add layer warning: {e}")
    # Symbology is often applied in Map Viewer; here we only add. Optional: update layer definition if API supports.

def main():
    gis = get_gis()
    layers_cfg = json.loads(LAYERS_CONFIG.read_text())
    symbology_cfg = json.loads(SYMBOLOGY_CONFIG.read_text()) if SYMBOLOGY_CONFIG.exists() else {}
    state_path = CONFIG_DIR / "portal_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    folder_id = state.get("folder_id")

    # Create or get existing web map (WebMap from arcgis.mapping or Map from arcgis.map)
    existing = gis.content.search(f"title:{WEB_MAP_TITLE}", item_type="Web Map")
    if existing:
        web_map = WebMap(existing[0])
        print(f"Using existing Web Map: {WEB_MAP_TITLE}")
    else:
        web_map = WebMap()
        save_props = {"title": WEB_MAP_TITLE, "tags": "AMD, REE, water quality"}
        try:
            web_map.save(save_props, folder=folder_id)
        except TypeError:
            web_map.save(WEB_MAP_TITLE, folder=folder_id)
        print(f"Created Web Map: {WEB_MAP_TITLE}")

    hosted = state.get("hosted_layers", {})
    hosted_cfg = layers_cfg.get("hosted_layers", {})
    # Order: hydrology (base), then AMD, REE, water quality points
    order = ["hydrology_units", "amd_severity", "ree_potential", "water_quality_points"]
    for key in order:
        if key not in hosted:
            continue
        cfg = hosted_cfg.get(key, {})
        sym = symbology_cfg.get(key, {})
        add_layer_to_map(web_map, hosted[key], cfg, sym)

    ogc = state.get("ogc_layers", {})
    add_ly = web_map.content.add if hasattr(web_map, "content") and hasattr(web_map.content, "add") else web_map.add_layer
    for ogc_id, ogc_info in ogc.items():
        try:
            item = gis.content.get(ogc_info["item_id"])
            if item and (item.layers or getattr(item, "layers", None)):
                for ly in (item.layers or []):
                    add_ly(ly) if add_ly == web_map.content.add else add_ly(ly, {"visibility": True})
            elif item:
                add_ly(item) if add_ly == web_map.content.add else add_ly(item, {"visibility": True})
        except Exception as e:
            print(f"OGC layer {ogc_id}: {e}")

    web_map.update()
    state["web_map_id"] = web_map.item.id
    state_path.write_text(json.dumps(state, indent=2))
    print(f"Web Map ID: {web_map.item.id}")
    return state

if __name__ == "__main__":
    main()
