# Data dictionary – AMD & REE portal

## Hosted layers (your data)

| Field | Layer(s) | Meaning |
|-------|----------|---------|
| amd_score | AMD Severity | Acid mine drainage severity score (0–100 or class). Higher = more severe. |
| severity_class | AMD Severity | Text class (e.g. Low / Medium / High). |
| ree_score | REE Potential | Rare earth element potential score (0–100 or class). |
| potential_class | REE Potential | Text class. |
| ph | Water Quality | pH (standard units). &lt; 7 = acidic; AMD-affected waters often &lt; 5. |
| conductivity | Water Quality | Specific conductance (µS/cm). Elevated with dissolved ions (e.g. sulfate). |
| sulfate_mgl | Water Quality | Sulfate (mg/L). Common AMD indicator. |
| iron_mgl | Water Quality | Iron (mg/L). Often elevated in AMD. |
| alkalinity | Water Quality | Alkalinity (mg/L as CaCO3). Buffering capacity. |
| sample_date, collection_datetime | Water Quality | When the sample was taken. |
| huc_code, huc_name | Hydrology Units | Hydrologic unit code and name (watershed). |

## USGS OGC API (live)

| Parameter / field | Meaning |
|-------------------|---------|
| parameter_code 00095 | Specific conductance (µS/cm). |
| parameter_code 00400 | pH. |
| parameter_code 00915 | Sulfate (mg/L). |
| parameter_code 00940 | Iron (mg/L). |
| parameter_code 29820 | Alkalinity (mg/L as CaCO3). |
| time | Observation date/time. |
| value | Numeric value for the parameter. |
| unit_of_measure | Unit (e.g. uS/cm, mg/L). |

**Update frequency**: Monitoring locations ~60 min; field measurements and daily values per `config/usgs_ogc_endpoints.json` (e.g. 30–60 min).
