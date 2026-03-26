#!/usr/bin/env python3
"""
Step 2: Publish processed feature datasets as Hosted Feature Layers.
Expects data in data/ as CSV (with lat/lon or geometry), Shapefile, or GeoJSON.
Enables Export Data (CSV, Shapefile, GeoJSON). Creates a Feature Layer View
per layer with filter for valid records.
"""
import json
from pathlib import Path

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, DATA_DIR, PORTAL_FOLDER, get_gis

LAYERS_CONFIG = CONFIG_DIR / "layers.json"


def _get_folder(gis, folder_id):
    """Return Folder object for portal folder or root."""
    if folder_id:
        return gis.content.folders.get(folder=PORTAL_FOLDER)
    return gis.content.folders.get()


def publish_from_file(gis, file_path, layer_key, layer_cfg, folder_id):
    """Publish one hosted feature layer from a file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    title = layer_cfg["title"]
    item_type = "Shapefile" if path.suffix.lower() == ".shp" else "CSV" if path.suffix.lower() == ".csv" else "GeoJSON"
    item_props = {
        "title": title,
        "tags": "AMD, REE, water quality, hosted",
        "type": item_type,
    }
    folder = _get_folder(gis, folder_id)
    try:
        from arcgis.gis import ItemProperties, ItemTypeEnum
        type_enum = getattr(ItemTypeEnum, item_type.upper().replace(" ", "_"), item_type)
        props = ItemProperties(title=title, item_type=type_enum, tags="AMD, REE, water quality, hosted", snippet=title)
    except (ImportError, AttributeError, TypeError):
        props = item_props
    add_result = folder.add(props, file=str(path))
    item = add_result.result() if hasattr(add_result, "result") else add_result
    try:
        published = item.publish()
    except Exception as e:
        item.delete()
        raise e

    # Enable export on the service
    flc = published.layers[0] if published.layers else published.tables[0]
    if hasattr(flc, "manager") and hasattr(flc.manager, "update_definition"):
        try:
            flc.manager.update_definition({"capabilities": "Query,Extract"})
        except Exception:
            pass

    # Create view with filter
    view_filter = layer_cfg.get("view_filter", "1=1")
    view_def = {"filter": view_filter} if view_filter and view_filter != "1=1" else None
    view_item = None
    if hasattr(published, "create_view") and view_def:
        try:
            view_item = published.create_view(name=f"{title} (View)", view_def=view_def)
        except Exception:
            pass

    return {"item": published, "view": view_item, "item_id": published.id}

def publish_from_sdf(gis, sdf, layer_key, layer_cfg, folder_id):
    """Publish from a Spatially-Enabled DataFrame."""
    title = layer_cfg["title"]
    item_props = {"title": title, "tags": "AMD, REE, water quality, hosted"}
    if folder_id:
        item_props["folder"] = folder_id
    item = gis.content.import_data(sdf, item_props)
    published = item.publish()
    # Enable export
    flc = published.layers[0] if published.layers else published.tables[0]
    if hasattr(flc, "manager") and hasattr(flc.manager, "update_definition"):
        try:
            flc.manager.update_definition({"capabilities": "Query,Extract"})
        except Exception:
            pass
    view_filter = layer_cfg.get("view_filter", "1=1")
    view_item = None
    if hasattr(published, "create_view") and view_filter and view_filter != "1=1":
        try:
            view_item = published.create_view(name=f"{title} (View)", view_def={"filter": view_filter})
        except Exception:
            pass
    return {"item": published, "view": view_item, "item_id": published.id}

def main():
    gis = get_gis()
    layers_cfg = json.loads(LAYERS_CONFIG.read_text())
    hosted = layers_cfg.get("hosted_layers", {})
    view_filters = layers_cfg.get("layer_view_filters", {})

    state_path = CONFIG_DIR / "portal_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    folder_id = state.get("folder_id")

    published = {}
    for key, cfg in hosted.items():
        cfg["view_filter"] = view_filters.get(key, "1=1")
        # Look for data file: data/amd_severity.csv, .shp, .geojson, etc.
        for ext in [".csv", ".shp", ".geojson", ".json"]:
            path = DATA_DIR / f"{key}{ext}"
            if path.exists():
                try:
                    result = publish_from_file(gis, path, key, cfg, folder_id)
                    published[key] = result
                    print(f"Published: {key} -> {result['item_id']}")
                except Exception as e:
                    print(f"Failed {key}: {e}")
                break
        else:
            print(f"No data file found for {key} in {DATA_DIR}; skipping.")

    state["hosted_layers"] = {k: v["item_id"] for k, v in published.items()}
    state_path.write_text(json.dumps(state, indent=2))
    return state

if __name__ == "__main__":
    main()
