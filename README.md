# slidev_talks

Lecture slides built with [Slidev](https://sli.dev). Published at
**https://willychap.github.io/slidev_talks/**. Every push to `main` rebuilds and redeploys them
(`.github/workflows/pages.yml`).

| Deck | Source | Theme | URL |
|---|---|---|---|
| Gregory diagrams | `gregory-atoc.md`, generated from `gregory/atoc_template.md` | `themes/atoc4870` (local) | `/slidev_talks/gregory/` |
| Gregory diagrams | `gregory-lecture.md` | `slidev-theme-cu-boulder` (npm, from GitHub) | `/slidev_talks/gregory-cu/` |

## Run locally

Requires Node 22 or later.

```bash
npm install
npm run atoc        # ATOC-style deck at http://localhost:3030
npm run gregory     # CU-style deck
npm run            # list all scripts
```

The scripts are defined in `package.json` under `"scripts"`. Their `PATH="$PWD/.node-env/bin:$PATH"`
prefix selects the conda Node 22 on NCAR Casper and does nothing elsewhere.

## Layout

```
gregory-lecture.md        CU deck; also the master copy of the speaker notes
gregory/atoc_template.md  ATOC deck source; edit this, then: python3 gregory/make_atoc_deck.py
gregory-atoc.md           generated ATOC deck (template + notes from gregory-lecture.md)
components/               interactive slides, auto-registered by Slidev
  GregoryExplorer.vue       CESM2 Gregory diagram with a selectable fitting window
  EBMExplorer.vue           0D / two-layer energy balance model with sliders
themes/atoc4870/          local theme matching the ATOC 4870 PowerPoint decks
public/figures/           static figures, served at /figures/...
style.css                 shared slide classes (.caption, .context, .fig-full, ...)
gregory/data/             CESM2 anomalies used by the components (bundled into the build)
gregory/analysis/         scripts that make the data and figures
gregory/pptx/             builds an editable PowerPoint version (python-pptx)
site/index.html           landing page listing the decks
```

## Data

CESM2 abrupt-4xCO2 and piControl, r1i1p1f1, CMIP6 (Danabasoglu, 2019).

1. `gregory/analysis/global_means.py` reads monthly `tas`, `rsdt`, `rsut`, `rlut` from the CMIP6 archive
   on NCAR Glade and writes annual global means to `cesm2_global_annual.csv` (included).
2. `gregory/analysis/make_figures.py` subtracts the piControl mean (control years 502–1200) and writes
   `gregory/data/*.json` and `public/figures/*.png`. It only needs the CSV, so it runs anywhere.

## Adding a deck

1. Write `mytalk.md` with `theme: ./themes/atoc4870` (or `cu-boulder`) and `routerMode: hash` in the
   headmatter.
2. Add a build line to `.github/workflows/pages.yml`:
   `npx slidev build mytalk.md --base /slidev_talks/mytalk/ --out _site/mytalk`
3. Add a link in `site/index.html`.
