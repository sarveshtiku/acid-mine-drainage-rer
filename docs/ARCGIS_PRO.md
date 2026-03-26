# Using the portal in ArcGIS Pro

- **Add the Web Map**: Insert → Maps → **Web Map**; sign in to your org and choose **AMD_REE_InteractiveMap**, or paste the map URL from DELIVERABLES.md.
- **Add USGS OGC API layers**: Map → Add Data → **Path** (or Add Data from Path). For OGC API – Features:
  - **Catalog** → Servers → **New OGC API Connection**.
  - URL: `https://api.waterdata.usgs.gov/ogcapi/v0` (or a specific collection, e.g. `.../collections/monitoring-locations`).
  - Add the connection, then expand and add the desired collections as layers.
- **Sync with AGOL**: Changes to the web map (symbology, popups) are saved in the cloud; opening the same web map in Pro shows the same layers. Hosted layers can be updated by overwriting from Pro or by running your publish script with updated data.
