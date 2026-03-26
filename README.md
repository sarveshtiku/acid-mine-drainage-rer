# AMD + REE Live Mapping and Dashboard (ArcGIS Online)

Build the **AMD (acid mine drainage) + REE (rare earth elements)** live mapping and dashboard in **ArcGIS Online** and **ArcGIS Pro** using USGS Water Data OGC API and your geoprocessed AMD/REE score data.

## Quick start

1. **Prerequisites**: ArcGIS Online org account, Python 3.8+, [ArcGIS API for Python](https://developers.arcgis.com/python/) (`pip install arcgis`).
2. **Sign in once**: `python -c "from arcgis.gis import GIS; GIS(profile='home')"` and complete login (browser or username/password).
3. **Add your data** under `data/`: see [data/README.md](data/README.md). Sample `water_quality_points.csv` is included.
4. **Run the pipeline**:
   ```bash
   pip install -r requirements.txt
   python scripts/run_all.py
   ```
   Or run steps individually: `01_project_setup.py` → `02_publish_hosted_layers.py` → `03_ogc_layers.py` → `04_web_map.py` → `05_dashboard.py` → `06_share_and_download.py`.

5. **Manual steps in AGOL** (if needed):
   - **Symbology**: In Map Viewer, set AMD layer to heatmap, REE to graduated colors, water quality to points, hydrology to outlines (see [config/symbology.json](config/symbology.json)).
   - **Popups**: Configure in Map Viewer per layer (field aliases in [config/layers.json](config/layers.json)).
   - **Dashboard**: If the script does not create the dashboard, open the Web Map → **Create App** → **Dashboards**; add Map, Indicators (e.g. count of high-severity reaches, average REE potential), Filters (date range, watershed), Charts/Tables; set table action to zoom map to record.
   - **OGC refresh**: For each USGS OGC layer, set refresh interval (e.g. 30–60 min) in layer properties in the map or in item settings.

## What the build does (steps 1–10)

| Step | Script / action | Result |
|------|------------------|--------|
| 1 | `01_project_setup.py` | Folder **AMD_REE_Portal**; standard metadata (title, summary, tags). |
| 2 | `02_publish_hosted_layers.py` | Hosted Feature Layers (AMD severity, REE potential, water quality points, hydrology); Export Data (CSV, Shapefile, GeoJSON); Feature Layer Views with filters. |
| 3 | `03_ogc_layers.py` | USGS OGC API – Features layers added from [api.waterdata.usgs.gov/ogcapi/v0](https://api.waterdata.usgs.gov/ogcapi/v0) (monitoring locations, field measurements, daily values). |
| 4 | `04_web_map.py` | Web Map **AMD_REE_InteractiveMap** with all layers; symbology and popups can be refined in Map Viewer. |
| 5 | `05_dashboard.py` | Dashboard from the web map (or instructions to create it manually with Map, Indicators, Filters, Charts/Tables, actions). |
| 6 | `06_share_and_download.py` | Web Map and Dashboard shared publicly; Export Data enabled on hosted layers. |
| 7 | Docs | [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md), [docs/ReadMe_layer_content.md](docs/ReadMe_layer_content.md); add ReadMe text to map. |
| 8 | Config | Refresh intervals in [config/usgs_ogc_endpoints.json](config/usgs_ogc_endpoints.json); republish hosted layers on your schedule (e.g. daily). |
| 9 | QA | Validate popups, filters, and downloads (CSV/GeoJSON/Shapefile) in Map Viewer and Dashboard; test in multiple browsers. |
| 10 | [docs/DELIVERABLES.md](docs/DELIVERABLES.md) | Fill in item URLs (from `config/portal_state.json`) for Web Map, Dashboard, each Hosted Layer, USGS OGC layers, and download links. |

## Project layout

```
config/           # Layer definitions, symbology, USGS OGC URLs, metadata defaults
data/             # Your feature data (CSV, Shapefile, GeoJSON)
docs/             # Data dictionary, ReadMe text, DELIVERABLES template
scripts/          # 01–06 Python scripts + run_all.py
```

## Configuration

- **ArcGIS profile**: Set `ARCGIS_PROFILE` (e.g. `home`) or use default.
- **USGS API key** (optional, for higher rate limits): Copy [.env.example](.env.example) to `.env` and set `USGS_API_KEY=your_key`. Never commit `.env`; it is gitignored. The key is used when adding OGC layers so AGOL can call USGS with the key.
- **Layers**: [config/layers.json](config/layers.json) – titles, id/date fields, aliases, view filters.
- **USGS OGC**: [config/usgs_ogc_endpoints.json](config/usgs_ogc_endpoints.json) – collection URLs, refresh minutes, popup fields.
- **Symbology**: [config/symbology.json](config/symbology.json) – heatmap (AMD), graduated (REE), point, outline.

## Maintenance

- **Hosted layers**: Re-run your geoprocessing; overwrite or append to the hosted layers (e.g. via ArcGIS API for Python or Pro), or republish from updated files with `02_publish_hosted_layers.py` (replace items as needed).
- **OGC layers**: Refresh interval is set in AGOL (e.g. 30–60 min) per layer.
- **Dashboard**: Edit in ArcGIS Dashboards; add download button linking to each hosted layer’s item page if desired.

## USGS OGC API + ArcGIS Online

USGS real-time water data is added as **OGC API – Features** layers. ArcGIS Online accepts the **items** endpoint (returns GeoJSON), e.g.:

- `https://api.waterdata.usgs.gov/ogcapi/v0/collections/latest-continuous/items?parameter-codes=00400,00095`
- **Add Item** → **From URL** → **OGC API-Features** → paste URL → add to Web Map → set refresh interval.

**Caveats:** ~3,000 features per request (use `limit` or `bbox` if needed); OGC layers are read-only; use Web Mercator for best display. Full workflow: [docs/USGS_ARCGIS_WORKFLOW.md](docs/USGS_ARCGIS_WORKFLOW.md).

## References

- [USGS Water Data OGC API](https://api.waterdata.usgs.gov/docs/ogcapi)
- [Add layers from URL (OGC API – Features)](https://doc.arcgis.com/en/arcgis-online/create-maps/add-layers-from-url.htm)
- [ArcGIS API for Python](https://developers.arcgis.com/python/)
- [Authoring ArcGIS Dashboards (Python)](https://developers.arcgis.com/python/guide/authoring-arcgis-dashboards/)
