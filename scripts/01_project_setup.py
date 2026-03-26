#!/usr/bin/env python3
"""
Step 1: Create ArcGIS Online workspace and folder.
- Connect to AGOL (org).
- Create folder "AMD_REE_Portal".
- Set standard metadata defaults for the folder (documented in config).
"""
import json
from pathlib import Path

# Add parent to path for env
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, PORTAL_FOLDER, get_gis


def main():
    gis = get_gis()
    meta_path = CONFIG_DIR / "metadata_defaults.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    # Create folder (idempotent: search first)
    # gis.users.me.folders yields Folder objects (.name and .properties), not dicts
    folders = gis.users.me.folders
    folder_id = None
    for f in folders:
        title = getattr(f, "name", None) or (f.properties or {}).get("title")
        if title == PORTAL_FOLDER:
            folder_id = (f.properties or {}).get("id")
            print(f"Folder already exists: {PORTAL_FOLDER} (id={folder_id})")
            break
    if folder_id is None:
        new_folder = gis.content.folders.create(PORTAL_FOLDER, exist_ok=True)
        folder_id = getattr(new_folder, "id", None) or (new_folder.properties or {}).get("id")
        print(f"Created folder: {PORTAL_FOLDER} (id={folder_id})")

    # Store for downstream scripts
    state_path = Path(__file__).resolve().parent.parent / "config" / "portal_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = {"folder_id": folder_id, "folder_name": PORTAL_FOLDER, "metadata_defaults": meta}
    state_path.write_text(json.dumps(state, indent=2))
    print("Portal state written to config/portal_state.json")
    return state

if __name__ == "__main__":
    main()
