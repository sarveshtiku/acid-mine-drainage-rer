# USGS OGC API + ArcGIS Online — Workflow & Caveats

## Can I load USGS real-time data directly into ArcGIS Online?

**Yes.** The USGS Water Data APIs support **OGC API – Features**, which ArcGIS Online can consume as a live vector layer. You get continuous sensor data, daily values, and monitoring metadata in a GIS-friendly format.

## How to add a USGS OGC API layer in ArcGIS Online

1. **Content** → **Add Item** → **From URL**.
2. Choose **OGC API-Features** as the type.
3. Paste a USGS endpoint that **returns features** (GeoJSON), e.g.:
   - `https://api.waterdata.usgs.gov/ogcapi/v0/collections/latest-continuous/items?parameter-codes=00400,00095`
   - `https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items`
4. Save the item, then add it to your Web Map.
5. In layer properties, set **Refresh interval** (e.g. 15–60 min) so the map stays current.
6. Configure **symbology** and **pop-ups** as needed.

## URL format ArcGIS Online accepts

Use the **items** endpoint so the response is GeoJSON:

```
https://api.waterdata.usgs.gov/ogcapi/v0/collections/{collection}/items
```

Optional query parameters:

- **parameter-codes** — e.g. `00400,00095` (pH, specific conductance) to limit to water-quality parameters.
- **limit** — cap number of features (see caveats below).
- **bbox** — bounding box to reduce features in a region.

Examples:

- Latest continuous (real-time), pH and conductivity only:  
  `.../collections/latest-continuous/items?parameter-codes=00400,00095`
- Daily values, same parameters:  
  `.../collections/daily/items?parameter-codes=00400,00095,00915,00940,29820`

## What the USGS OGC API provides

- **Continuous / latest-continuous** — real-time sensor values.
- **Daily** — daily aggregates (e.g. mean, min, max).
- **Monitoring locations** — site metadata (name, lat/lon, HUC).
- **Field measurements** — discrete water-quality measurements from site visits.

So you can show real-time pH, conductivity, and other parameters in your Web Map and dashboard.

## ArcGIS Pro

ArcGIS Pro can add **OGC API – Features** layers as read-only layers: connect to the OGC API server, pick the collection/items URL, add to the map, symbolize, then publish to ArcGIS Online if desired.

## Caveats

| Caveat | Detail |
|--------|--------|
| **Feature limit** | ArcGIS Online may only retrieve ~3,000 features per request. Use `limit` or `bbox` (or both) in the URL to stay under. |
| **Read-only** | OGC API layers are read-only in ArcGIS Online — no editing, only symbolize and query. |
| **Projection** | For best display in web maps, the layer’s coordinate system should align with Web Mercator. |

## Summary

- Use **items** URLs: `https://api.waterdata.usgs.gov/ogcapi/v0/collections/{id}/items` (with optional `parameter-codes`, `limit`, `bbox`).
- In ArcGIS Online: **Add Item** → **From URL** → **OGC API-Features**.
- Add the item to your Web Map, set refresh interval, and configure pop-ups.
- Use the same layers in dashboards; enable export only on **your** hosted layers (USGS layers are read-only).

This gives you live USGS water data in the AMD/REE map and dashboard without manual CSV uploads.
