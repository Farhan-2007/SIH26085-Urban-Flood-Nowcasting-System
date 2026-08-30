// Data access layer for the Urban Flood Nowcasting Dashboard.
//
// This talks to the real Flask backend (backend/app.py, registered at
// url_prefix="/api"). Every other part of the frontend goes through the
// functions exported here rather than calling fetch() directly, so the
// API integration lives in exactly one place.
//
// INSPECTION NOTES (read before changing this file):
//
// - GET /api/forecast always returns the forecast for the backend's
//   hardcoded SAMPLE_STREET/SAMPLE_WEATHER (backend/predictor.py). It does
//   not accept a location parameter, so it cannot power location
//   selection and is intentionally not used here.
//
// - POST /api/analyse (backend/api/routes.py) is the endpoint that
//   actually ties a real location_id to a live analysis *and* the full
//   0/30/60/120/180-minute forecast (via backend/Analyser.py +
//   backend/predictor.py). This is the endpoint the dashboard is built
//   around.
//
// - /api/analyse requires a weather observation in the POST body
//   (rainfall, water_level, soil_saturation, lightning). No endpoint
//   currently serves that reading for a given location, so it's supplied
//   from the project's real dataset in src/data/locations.js (see that
//   file's header for why).
//
// - The backend's analyser is stateful per location_id (EMA smoothing +
//   trend detection carry over between calls on the server), so calling
//   this repeatedly for the same location will show "Stable" trends
//   after the first call, which is the correct, real behaviour of
//   backend/Analyser.py — not a frontend bug.

const API_BASE_URL = "http://localhost:5000/api";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function postJson(path, body) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (networkError) {
    throw new ApiError("Unable to reach the flood-risk service.", 0);
  }

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    // non-JSON response, fall through to status check below
  }

  if (!response.ok) {
    throw new ApiError(payload?.error || `Request failed (${response.status})`, response.status);
  }

  return payload;
}

// Calls POST /api/analyse for a given location using that location's
// real environmental snapshot as the "current observation". Returns the
// backend's { analysis, forecast } payload unchanged.
export async function analyseLocation(location) {
  const body = {
    location_id: location.locationId,
    rainfall: location.rainfall,
    water_level: location.waterLevel,
    soil_saturation: location.soilSaturation,
    lightning: false, // no live lightning sensor/data source currently available
  };

  return postJson("/analyse", body);
}

export { ApiError };
