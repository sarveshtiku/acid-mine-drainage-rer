# AMD + REE Portal – Deliverables

After running the build scripts (or manual setup), fill in the URLs below. Base URL format: `https://<org>.maps.arcgis.com/...` or your portal base.

## Summary list

| Item | URL |
|------|-----|
| **Web Map** | [AMD_REE_InteractiveMap](PLACEHOLDER_WEB_MAP_URL) |
| **Dashboard** | [AMD & REE Live Mapping Dashboard](PLACEHOLDER_DASHBOARD_URL) |
| **Hosted – AMD Severity** | PLACEHOLDER_AMD_LAYER_URL |
| **Hosted – REE Potential** | PLACEHOLDER_REE_LAYER_URL |
| **Hosted – Water Quality Points** | PLACEHOLDER_WQ_LAYER_URL |
| **Hosted – Hydrology Units** | PLACEHOLDER_HYDRO_LAYER_URL |
| **USGS – Monitoring Locations** | PLACEHOLDER_OGC_MONITORING_URL |
| **USGS – Field Measurements** | PLACEHOLDER_OGC_FIELD_URL |
| **USGS – Daily Values** | PLACEHOLDER_OGC_DAILY_URL |

## Downloadable data links

Each hosted feature layer has **Export Data** enabled (CSV, Shapefile, GeoJSON). Use the layer item page in ArcGIS Online:

- Open the layer item → **Export Data** or use the **View** (Feature Layer View) item if created.

## How to get URLs

- **portal_state.json**: After running the scripts, `config/portal_state.json` contains `item_id` values for map, dashboard, and layers.  
  Item URL form: `https://<org>.maps.arcgis.com/home/item.html?id=<item_id>`
- **REST URLs**: For hosted layers, the Feature Service URL is in the item’s **URL** field (e.g. `.../rest/services/.../FeatureServer/0`).

Replace each `PLACEHOLDER_*` above with the actual link once the build is complete.
