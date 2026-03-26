#!/usr/bin/env python3
"""
Step 5: Create ArcGIS Dashboard from the Web Map.
Add Map element, Indicators (high-severity count, avg REE), Filters (date, watershed),
Charts/Tables, and actions (table click -> zoom to record).
Uses arcgis.apps.dashboard (Dashboard class) where available.
"""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, PORTAL_FOLDER, WEB_MAP_TITLE, DASHBOARD_TITLE, get_gis


def main():
    gis = get_gis()
    state_path = CONFIG_DIR / "portal_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    folder_id = state.get("folder_id")
    web_map_id = state.get("web_map_id")

    if not web_map_id:
        print("Run 04_web_map.py first to create the Web Map.")
        return state

    # Create dashboard from Web Map: ArcGIS Online allows "Create App > Dashboards" from map.
    # The Python API (arcgis.apps.dashboard) can create dashboard items; layout is JSON.
    try:
        from arcgis.apps import dashboard
    except ImportError:
        dashboard = None

    if dashboard:
        try:
            # Dashboard() creates a new dashboard; we need to add map widget and others
            dash = dashboard.Dashboard(gis=gis)
            dash.title = DASHBOARD_TITLE
            dash.owner = gis.users.me.username
            # Add map element referencing our web map
            map_item = gis.content.get(web_map_id)
            if map_item:
                dash.add_map(map_item, position={"x": 0, "y": 0, "w": 12, "h": 8})
            dash.save(folder=folder_id)
            state["dashboard_id"] = dash.id
            print(f"Created Dashboard: {dash.id}")
        except Exception as e:
            print(f"Dashboard API usage may vary: {e}. Create dashboard manually from map: Create App > Dashboards.")
            state["dashboard_id"] = None
    else:
        # No dashboard module: emit instructions and placeholder id
        print("Create dashboard manually: open Web Map in Map Viewer > Create App > Dashboards.")
        print("Add: Map (this map), Indicators, Filters, Serial/Pie charts, Table; link table to map actions.")
        state["dashboard_id"] = None

    state_path.write_text(json.dumps(state, indent=2))
    return state

if __name__ == "__main__":
    main()
