# Data for AMD_REE_Portal

Place your geoprocessed feature datasets here so `02_publish_hosted_layers.py` can publish them as hosted feature layers.

## Expected files

| Layer key            | Suggested filename(s)                    | Geometry   | Required fields (examples) |
|----------------------|------------------------------------------|------------|----------------------------|
| amd_severity         | `amd_severity.csv`, `.shp`, or `.geojson` | Polygon    | amd_score, reach_id, (geometry or lat/lon) |
| ree_potential        | `ree_potential.csv`, `.shp`, or `.geojson`| Polygon    | ree_score, reach_id, (geometry or lat/lon) |
| water_quality_points | `water_quality_points.csv`, `.shp`, `.geojson` | Point   | site_id, sample_date, ph, (geometry or lat/lon) |
| hydrology_units      | `hydrology_units.csv`, `.shp`, or `.geojson` | Polygon  | huc_code, huc_name, (geometry) |

- **CSV**: must include `latitude`/`longitude` (or `lat`/`lon`, or `y`/`x`) for point data; for polygons use Shapefile or GeoJSON.
- **Shapefile**: include `.shp` (and `.shx`, `.dbf`, etc.) in the same folder.
- **GeoJSON**: single file with `geometry` in each feature.

Field aliases and view filters are defined in `config/layers.json`.
