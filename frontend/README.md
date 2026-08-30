# SIH26085 — Urban Flood Nowcasting System (Frontend)

Frontend dashboard for the Urban Flood Nowcasting System (Ministry of Earth
Sciences), integrated with the real Flask backend.

## Running locally

You need both the backend and frontend running.

**Backend** (from the repo root, so `backend` and `routing` resolve as packages):

```bash
pip install flask flask_cors pandas
python -m backend.app
```

This starts Flask on `http://localhost:5000`.

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Open the printed local URL (typically `http://localhost:5173`). The header's
status dot reflects the real connection to the backend — green when
`/api/analyse` succeeds, red if the backend isn't reachable.

## How the integration works

The dashboard is built around **`POST /api/analyse`** — the only backend
endpoint that ties a real `location_id` to both a live analysis and the
full 0/30/60/120/180-minute forecast (`backend/Analyser.py` +
`backend/predictor.py`).

`GET /api/forecast` was intentionally **not** used: as currently written it
always returns the forecast for the backend's hardcoded example street
(`SAMPLE_STREET`/`SAMPLE_WEATHER` in `backend/predictor.py`) and ignores any
location parameter, so it can't power location selection.

```
Location selector (src/data/locations.js)
        ↓
POST /api/analyse  { location_id, rainfall, water_level, soil_saturation, lightning }
        ↓
{ analysis: {...}, forecast: [5 points] }   (src/services/api.js)
        ↓
useFloodData hook (src/hooks/useFloodData.js)
        ↓
Dashboard components
```

### Why location data is bundled in the frontend

No current endpoint lists locations or returns a location's current
rainfall/water-level/soil-saturation reading — `backend/data_loader.py`'s
`get_location()` only returns lat/lon plus the same hardcoded
infrastructure values for every location, ignoring `data/raw/flood_features.csv`
entirely.

`src/data/locations.js` bundles the real values from `locations.csv` and
`flood_features.csv` as the "current observation" sent to `/api/analyse`,
since that's the project's actual dataset — not invented numbers. If the
team adds an endpoint that serves this instead, replace that file's export
with a fetch call and keep the same field names; no component changes
needed.

### A note on risk-level labels

`backend/flood_engine/risk_calculator.py` (used by `POST /api/predict`)
returns `LOW/MEDIUM/HIGH/CRITICAL`, while the forecast engine used by
`/api/analyse` (`backend/predictor.py`) returns `Low/Moderate/High/Critical`.
`src/utils/riskLevel.js` normalizes whichever string the backend returns
into one consistent uppercase vocabulary for display — it does not
recompute the risk level itself.

### A note on what actually updates with the forecast timeline

The backend's forecast only recomputes **rainfall, surface runoff, drainage
capacity used, and excess water** per forecast step. It does not return a
forecasted water level or soil saturation. The Risk Factors panel reflects
this honestly: "Forecast Conditions" (rainfall, runoff, drainage, excess
water) update when the timeline moves; "Current Observed Conditions"
(channel fill level, soil saturation) are shown as live-only readings that
don't change with the timeline.

## Known gap: the routing module isn't wired to real flood data

`backend/api/routes.py`'s `/api/routing` endpoint calls
`routing_engine.build_routing_report(start_id, end_id)` with no other
arguments, so per `routing/routing_engine.py`'s `load_mock_inputs()`, it
always falls back to `routing/mock_data.py`'s `MOCK_LOCATIONS` /
`MOCK_RISK_DATA` — a fictional Bangalore location set (`L1`–`L10`,
Koramangala, Silk Board, etc.) with no relationship to the real flood
dataset's locations (`L001`–`L010`, Mumbai).

The frontend does not currently display road-impact/routing information,
because doing so today would either show unrelated Bangalore road names
next to real Mumbai flood data, or fail outright for every real location
ID. Once the backend passes real `locations`/`roads`/`risk_data` into
`build_routing_report` (or the location ID schemes are unified), a "Road
Impact" section can be added the same way the rest of this dashboard
consumes `/api/analyse` — through `src/services/api.js`, without touching
`routing/*`.

## Project structure

```
src/
├── components/     UI components (one file + one CSS file per component)
├── data/           locations.js — real project location + snapshot data
├── services/       api.js — the only file that calls fetch()
├── hooks/          useFloodData.js — location state, fetch, forecast step
├── utils/          riskLevel.js, formatValue.js, generateAlerts.js, forecastLabels.js
├── App.jsx         page composition, loading/error states
└── main.jsx        entry point
```

## Testing checklist (verified against the real backend)

- Dashboard loads and connects to `/api/analyse` — verified via live browser test
- Switching locations via the dropdown or map updates every panel
- Selecting a high-rainfall location (e.g. Sample Road 10) produces a real
  HIGH risk score, drainage-exceeded state, and dynamically generated alerts
- Moving the forecast timeline updates the gauge, factors, rainfall chart,
  and map consistently (map risk level now follows the selected forecast
  step, not always "now")
- Backend unreachable → error state with retry, no stale/fake data shown
- Invalid location handling verified against the backend's real 404 response
- No console errors during a full location-switch + timeline-scrub session
- Responsive down to 390px mobile width
