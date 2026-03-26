#!/usr/bin/env python3
"""
Generate docs/DELIVERABLES.md with real item URLs from config/portal_state.json.
Run after run_all.py (or after manual setup with portal_state.json populated).
"""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from env import CONFIG_DIR, get_gis


def main():
    gis = get_gis()
    state_path = CONFIG_DIR / "portal_state.json"
    if not state_path.exists():
        print("Run 01_project_setup.py (or run_all.py) first.")
        return
    state = json.loads(state_path.read_text())
    base = gis.url.rstrip("/")
    # Portal item URL pattern (AGOL)
    def item_url(iid):
        if not iid:
            return "PLACEHOLDER"
        return f"{base}/home/item.html?id={iid}"

    web_map_url = item_url(state.get("web_map_id"))
    dashboard_url = item_url(state.get("dashboard_id"))
    hosted = state.get("hosted_layers", {})
    ogc = state.get("ogc_layers", {})

    lines = [
        "# AMD + REE Portal – Deliverables",
        "",
        "## Summary list",
        "",
        "| Item | URL |",
        "|------|-----|",
        f"| **Web Map** | [AMD_REE_InteractiveMap]({web_map_url}) |",
        f"| **Dashboard** | [AMD & REE Live Mapping Dashboard]({dashboard_url}) |",
    ]
    for key, iid in hosted.items():
        label = key.replace("_", " ").title()
        lines.append(f"| **Hosted – {label}** | {item_url(iid)} |")
    for key, info in ogc.items():
        title = (info.get("title") or key).replace("_", " ").title()
        lines.append(f"| **USGS – {title}** | {item_url(info.get('item_id'))} |")

    lines.extend([
        "",
        "## Downloadable data",
        "",
        "Each hosted feature layer has **Export Data** enabled (CSV, Shapefile, GeoJSON). Open the layer item page above and use **Export Data**.",
        "",
        "---",
        f"*Generated from {state_path.name}*",
    ])

    out_path = Path(__file__).resolve().parent.parent / "docs" / "DELIVERABLES.md"
    out_path.write_text("\n".join(lines))
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
