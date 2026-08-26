# SIH26085 — Urban Flood Nowcasting System (Frontend)

Frontend dashboard prototype for **Urban Flood Nowcasting System — Drainage and
Rainfall Coupling**, built for the Smart India Hackathon internal round
(Ministry of Earth Sciences).

## Running locally

```bash
cd frontend
npm install
npm run dev
```

The dev server prints a local URL (typically `http://localhost:5173`).

To produce a production build:

```bash
npm run build
npm run preview   # serves the built files locally for a final check
```

## Project structure

```
src/
├── components/     UI components (one file + one CSS file per component)
├── data/           mockData.js — all mock/demo data lives here
├── services/       api.js — data-access layer; swap in real API calls here
├── hooks/          useDashboardData.js — loads data via services/api.js
├── utils/          riskLevel.js — score → risk level conversion
├── App.jsx         page composition / layout
└── main.jsx        entry point
```

## Replacing mock data with the real backend

Every dashboard component reads data through `src/services/api.js`, never
directly from `src/data/mockData.js`. When the backend API is ready:

1. Update the function bodies in `src/services/api.js` to call the real
   endpoints (e.g. `fetch("/api/risk/current")`) instead of resolving the
   mock objects.
2. Keep the returned shape the same as what's currently in
   `src/data/mockData.js` — components are written against that shape.
3. No component code should need to change.

## Risk level thresholds

`src/utils/riskLevel.js` converts a 0–100 risk score into
LOW / MODERATE / HIGH / CRITICAL. Thresholds are defined once in
`RISK_THRESHOLDS` and used everywhere a risk level is displayed (gauge,
badges, map legend, forecast timeline) — adjust them there if the
backend team's model uses different bands.

## Map component

`src/components/FloodMap.jsx` currently renders a schematic placeholder
with mock risk-zone markers (`src/data/mockData.js` → `RISK_ZONES`). It's
isolated specifically so it can be swapped for a real GIS/mapping
implementation (e.g. Leaflet or Mapbox) without touching how the rest of
the dashboard supplies zone data.

## Notes

- All data on screen is mock/prototype data, clearly labelled as such in
  the UI (see the "Prototype Data (Mock)" tag in the system info bar).
- No backend or GIS integration is wired up yet — this is a frontend-only
  prototype for the internal-round demo.
