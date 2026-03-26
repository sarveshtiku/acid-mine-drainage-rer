# AMD & Rare Earth Elements Spatial Intel Platform
### West Virginia Acid Mine Drainage & Rare Earth Element Mapping

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![ArcGIS](https://img.shields.io/badge/ArcGIS-Online-2C7AC3?style=flat-square&logo=esri&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

<img width="1351" height="726" alt="Screenshot 2026-03-26 at 15 36 25" src="https://github.com/user-attachments/assets/d36b4e94-1d71-4e96-bb3c-eed2c29882d3" />

## Overview

A full-stack geospatial pipeline that transforms raw water chemistry data into actionable decision-support maps for AMD remediation and REE recovery in West Virginia. Built on a custom multi-factor scoring model, IDW spatial interpolation, and ArcGIS Online as the deployment layer.

The goal: help field teams (boots on the ground) prioritize where to test, monitor, and intervene, with transparent methods and downloadable outputs.


## The Problem

West Virginia's legacy mining footprint continuously degrades stream chemistry. AMD lowers pH and concentrates dissolved metals, harming ecosystems and water usability across entire watersheds.

At the same time, AMD-impacted waters carry REE signals that may support domestic critical-mineral recovery, if extraction conditions are right.

The challenge is operational, not just scientific:

| Stakeholder | Need |
|---|---|
| Field teams | Clear spatial picture of worst contamination |
| Planners | Downloadable data, not one-off analyses |
| Stakeholders | Transparent metrics, not black-box maps |

## Scoring Model

### Normalization

All variables are normalized to [0, 1] for cross-parameter comparability:

$$\tilde{x}_i = \frac{x_i - \min(x)}{\max(x) - \min(x)}$$

For pH, lower values indicate higher acidity risk — so the scale is inverted:

$$\widetilde{pH}^{risk}_i = \frac{\max(pH) - pH_i}{\max(pH) - \min(pH)}$$


### AMD Severity Score

Weighted linear combination across five chemistry parameters:

$$S_i^{AMD} = 0.30\,\widetilde{pH}^{risk}_i + 0.20\,\widetilde{SO_4}_i + 0.20\,\widetilde{Fe}_i + 0.15\,\widetilde{Al}_i + 0.15\,\widetilde{Mn}_i$$

| Parameter | Weight | Rationale |
|---|---|---|
| pH (inverted) | 0.30 | Primary acidity driver |
| SO4 | 0.20 | Sulfate — AMD proxy |
| Fe | 0.20 | Iron — mobilization indicator |
| Al | 0.15 | Aluminum toxicity |
| Mn | 0.15 | Manganese — downstream risk |

Higher score = stronger contamination intensity.


### REE Opportunity Score

$$S_i^{REE} = 0.45\,\widetilde{REE}_{source,i} + 0.25\,\widetilde{pH}^{extract}_i - 0.30\,\widetilde{C}^{comp}_i$$

Where competitive cation burden is:

$$C_i^{comp} = Ca_i + Fe_i + Al_i + Mn_i + K_i + Mg_i + Na_i$$

Higher score = better extraction feasibility. The penalty term captures competing ions that reduce REE separation efficiency.


### Spatial Interpolation (IDW)

Point scores are interpolated to continuous surfaces using Inverse Distance Weighting:

$$\hat{S}(x) = \frac{\displaystyle\sum_i \frac{S_i}{d(x,\, x_i)^2}}{\displaystyle\sum_i \frac{1}{d(x,\, x_i)^2}}$$

This enables watershed-level prioritization rather than site-by-site inspection.


## Technical Stack

| Layer | Tool |
|---|---|
| Data ingestion | USGS Water Quality Portal (WQP), OGC services |
| Processing & scoring | Python 3.12, pandas, numpy |
| Geospatial ops | ArcGIS API for Python, shapely |
| Interpolation | IDW via ArcGIS spatial analyst |
| Deployment | ArcGIS Online (hosted feature layers + web maps) |
| Frontend | HTML/JS — embedded ArcGIS experience |

## Research Depth: Methods Explored

This was not a one-tool build. Several technical approaches were worked through to build real process intuition before converging on ArcGIS Online as the deployment platform.

### Hydraulic & Floodplain Modeling (HEC-RAS style)

Flow patterns, velocity distributions, and inundation behavior in valley systems. Providing process-level intuition for how contaminated water moves and where monitoring should concentrate.

![HEC-RAS style hydraulic mapping workflow](website-images/Trail-2.png)

### Cartographic & Terrain Context (Legacy ArcMap style)

Layer stacks, basemap interpretation, scale-aware cartography, and thematic overlays. Used to refine visual storytelling before building the public-facing product.

![Legacy ArcMap-style cartographic workflow](website-images/Trail-1.png)

### USGS Provisional Data Workflow

Station-level parameter retrieval, time-window queries, and export-driven review — grounding the model in real field data quality constraints and temporal gap analysis.

![USGS provisional station data workflow](website-images/Provisional-Data.png)

### Final Integration: ArcGIS Online

After these stages, ArcGIS Online was selected for:
- Compositing spatial layers (risk + opportunity + watershed context)
- Popups and dashboards for non-technical interpretation
- Public sharing and export for real partner collaboration

---

## Key Engineering Challenges

**ArcGIS auth complexity (org + SSO)**
Moved from one-shot automation to a hybrid workflow: scripted where reliable, AGOL UI where faster and more stable.

**USGS OGC ingestion instability in AGOL**
Switched to WQP/CSV-hosted layer workflows when direct OGC item behavior was inconsistent.

**API/library compatibility**
Updated scripts for newer ArcGIS API patterns and added defensive fallbacks for version drift.

**Data availability gaps**
Used publicly available WV-focused water quality sources and structured sample data to maintain forward progress.


## Broader Context

This work aligns with growing evidence that AMD streams can be both an environmental liability and a domestic critical-mineral resource. See Yale E360: [In Hunt for Rare Earths, Companies Are Scouring Mining Waste](https://e360.yale.edu/features/mining-waste-rare-earth-minerals) — including WV pilot efforts and policy/monitoring caveats.

---

> Built to turn fragmented chemistry and location data into a practical spatial workflow for remediation and monitoring prioritization in West Virginia.
