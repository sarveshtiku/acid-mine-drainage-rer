# ReadMe layer – Project purpose and data interpretation

Use this text as the **ReadMe** layer or description in the map (e.g. a text panel or the map’s item description).

---

## AMD & REE Live Mapping and Dashboard

This map shows **acid mine drainage (AMD)** severity and **rare earth element (REE)** potential along with **water quality** sample points and **USGS live** monitoring data.

### Layers

- **AMD Severity** – Geoprocessed scores by reach (heatmap). Higher values = greater AMD severity.
- **REE Potential** – Geoprocessed REE potential by unit (graduated colors).
- **Water Quality Sample Points** – Your discrete samples (pH, conductivity, sulfate, iron, alkalinity).
- **Hydrology Units** – Watershed boundaries (HUC) for context.
- **USGS Monitoring Locations / Field Measurements / Daily Values** – Live USGS OGC API layers; refresh every 30–60 minutes.

### Chemistry

- **pH** – &lt; 7 = acidic; AMD sites often &lt; 5.
- **Conductivity** – µS/cm; elevated with dissolved ions (e.g. sulfate from AMD).
- **Sulfate, Iron** – Common AMD indicators.
- **Alkalinity** – Buffering capacity (mg/L as CaCO3).

### Data sources

- Hosted layers: your geoprocessed datasets (see DATA_DICTIONARY.md).
- Live data: [USGS Water Data OGC API](https://api.waterdata.usgs.gov/docs/ogcapi).

### Updates

- Hosted layers: update and republish from your local pipelines (e.g. daily).
- USGS layers: automatic refresh per layer (see config).
