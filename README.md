<p align="center"><img src="assets/formula_one_logo.jpg" alt="Formula 1 Analytics" width="320"></p>

<p align="center"><strong>74 seasons of F1 history, live session telemetry, and a five-algorithm clustering sandbox — one Streamlit app.</strong></p>

<p align="center">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/streamlit-app-FF4B4B?logo=streamlit&logoColor=white"></a>
  <a href="https://docs.fastf1.dev/"><img alt="FastF1" src="https://img.shields.io/badge/FastF1-live%20telemetry-E10600"></a>
  <a href="https://plotly.com/python/"><img alt="Plotly" src="https://img.shields.io/badge/Plotly-visualizations-3F4F75?logo=plotly&logoColor=white"></a>
  <a href="https://scikit-learn.org/"><img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-clustering-F7931E?logo=scikitlearn&logoColor=white"></a>
  <a href="https://umap-learn.readthedocs.io/"><img alt="UMAP" src="https://img.shields.io/badge/UMAP-dim.%20reduction-4B0082"></a>
</p>

<p align="center">
  <a href="https://f1analytics.streamlit.app/">Live Demo</a> ·
  <a href="https://rafaelcoelho.pages.dev/work/formula-one-analytics">Portfolio Page</a> ·
  <a href="./F1Analytics.pdf">PDF Presentation</a>
</p>

---

## Table of Contents

- [What is this?](#what-is-this)
- [The five sections](#the-five-sections)
- [Key Components](#key-components)
- [Shipped but disabled: an early LLM experiment](#shipped-but-disabled-an-early-llm-experiment)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Author](#author)

---

## What is this?

Formula 1 Analytics covers 74 seasons of F1 history (1950–2023) through two complementary data sources: a static historical dataset (the classic Ergast/Kaggle F1 schema — circuits, constructors, drivers, results, lap times, pit stops) for anything season-spanning, and **FastF1**'s live API for session-level telemetry — actual gear shifts, tyre strategies, and speed traces from a specific race weekend. The platform is **publicly live** at [f1analytics.streamlit.app](https://f1analytics.streamlit.app/).

It was also a deliberate sandbox: every clustering algorithm, scaler, and dimensionality-reduction technique in AI Space was evaluated here against real F1 data before being considered for other work.

## The five sections

| Section | What it covers | Data source |
|---|---|---|
| **Overview** | Every circuit, constructor, driver, and race since 1950 — choropleth maps, country/continent breakdowns, searchable tables | Static historical dataset |
| **Insights** | Cross-filtered analysis: pick a circuit/constructor/driver and see its winning breakdown, nationalities, and fastest-lap record | Static historical dataset |
| **Seasons** | Session-level telemetry for a chosen season/race/session — track maps, gear shifts, tyre strategy, speed traces | **FastF1** (live) + **Ergast** (via FastF1's wrapper) |
| **AI Space** | Interactive clustering sandbox over race-result features — 5 algorithms × 4 scalers × 2D/3D UMAP | Static historical dataset |
| **About** | Author info | — |

## Key Components

### Insights' live Champions timeline

The Champions tab doesn't use the static dataset at all for its title list — it scrapes the current [F1 Champions table](https://f1.fandom.com/wiki/List_of_World_Drivers%27_Champions) directly via `pd.read_html()` on every page load, merges it with local driver data for nationality flags, and renders every champion from 1950 to today on an interactive [`streamlit-timeline`](https://github.com/innerdoc/streamlit-timeline) component with driver photos.

### Seasons' FastF1-powered telemetry

This is the section that actually calls a live external API, cached locally (`fastf1.Cache.enable_cache`). Pick a season, race, and session (Practice, Qualifying, Sprint, Race), and get ten distinct visualizations built from real telemetry:

- Track map with numbered corner annotations, correctly rotated to the circuit's actual orientation
- Gear-shift visualization painted directly onto the track shape
- Lap-by-lap position changes for every driver
- Full-season driver standings heatmap (via `Ergast`, with sprint-race points correctly merged into race points)
- Overlaid speed traces comparing any subset of drivers' fastest laps
- Team pace comparison (box plot of race-lap times by team)
- Tyre strategy Gantt chart (stint length by compound, stacked per driver)
- Speed trace with corner markers for the fastest lap
- Qualifying gap-to-pole bar chart
- Per-driver lap-time distribution (violin + compound-colored scatter)
- A dedicated per-driver tab: that driver's own tyre-strategy scatter plot and a track map painted by speed rather than gear

### AI Space's clustering sandbox

Every run scales the same race-result feature set with a chosen scaler (Standard / MinMax / Robust / Normalizer), projects it into both 2D and 3D with UMAP, then clusters the projection with a chosen algorithm — KMeans, Mean Shift (automatic bandwidth estimation), Agglomerative Clustering (optional k-NN connectivity graph, four linkage types), Bisecting KMeans, or OPTICS. Silhouette, Calinski-Harabasz, and Davies-Bouldin scores are computed live for whichever configuration is currently selected — they're diagnostics for exploring the parameter space, not fixed benchmarks for one "correct" clustering.

## Shipped but disabled: an early LLM experiment

`pages/ai_space.py` has a commented-out second tab (`#tabs = st.tabs(["Clustering", "LLM"])`) that was meant to let users chat with the race-results dataset in natural language. The exploration lives in `preprocessing/llm1.ipynb`: attempts against a local HuggingFace inference server (connection refused — server wasn't running), `HuggingFaceHub` (missing API token), a local Falcon-40B via `transformers`, and `pandasai` backed by OpenAI (quota exceeded) — every attempt failed at the time and none shipped. The same idea — chat with a dataframe via an LLM agent — later shipped successfully as [COELHO GenAI](https://github.com/rafaelcoelho1409/COELHOGenAI)'s Data Science tool.

## Tech Stack

| Technology | Role |
|---|---|
| **Streamlit** | UI shell, tabs, filters, maps |
| **FastF1** | Live session telemetry, lap data, tyre/gear/speed data |
| **Plotly** (`express`, `graph_objects`) | Choropleth maps, pies, box/violin plots, 2D/3D scatter |
| **Matplotlib** | Track-map and speed-heatmap rendering (`LineCollection`-based) |
| **pandas / NumPy** | Data wrangling across both static and live sources |
| **scikit-learn** | 5 clustering algorithms, 4 scalers, cluster-quality metrics |
| **UMAP** | 2D/3D dimensionality reduction ahead of clustering |
| **streamlit-timeline** | Interactive Champions-through-the-years timeline |

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python** 3.10+ | |
| A **Mapbox** access token | Set as the `MAPBOX_TOKEN` environment variable — required for every choropleth/scatter map in Overview and Insights |

## Installation

```bash
git clone https://github.com/rafaelcoelho1409/FormulaOneAnalytics
cd FormulaOneAnalytics

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export MAPBOX_TOKEN=your_mapbox_token_here
streamlit run app.py
```

FastF1 caches session data locally on first fetch (`./cache_fastf1`) — later requests for the same session are instant.

## Project Structure

```
FormulaOneAnalytics/
├── app.py                      # Home page — section overview, carousel
├── functions.py                  # Shared helpers, FastF1/Ergast wrappers, clustering pipeline
├── pages/
│   ├── overview.py                # Circuits/Constructors/Drivers/Races (historical)
│   ├── insights.py                # Cross-filtered analysis + live Champions timeline
│   ├── seasons.py                 # FastF1 session telemetry
│   ├── ai_space.py                 # Clustering sandbox (LLM tab commented out)
│   └── about.py                   # Author info
│
├── data/                        # Historical F1 dataset (Ergast/Kaggle schema, CSV + pickled)
├── preprocessing/                # Data-prep notebooks, including the abandoned llm1.ipynb
├── assets/                      # Logo, screenshots, driver/constructor images
│
├── F1Analytics.pdf               # Deployment record / demo deck
└── requirements.txt
```

## Author

**Rafael Coelho** — [rafaelcoelho.pages.dev](https://rafaelcoelho.pages.dev/)
