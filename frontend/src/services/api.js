// Data access layer for the Urban Flood Nowcasting Dashboard.
//
// UI components access dashboard data through the functions exported
// from this file. Mock data is still used for dashboard sections that
// are not connected to the backend yet.
//
// The flood-risk prediction is now connected to the Flask backend.

import {
  SYSTEM_INFO,
  FORECAST_TIMELINE,
  RAINFALL_HISTORY,
  ALERTS,
  RISK_ZONES,
  LAST_UPDATED,
} from "../data/mockData";

// Flask backend API
const API_BASE_URL = "http://127.0.0.1:5000/api";

// Simulates network latency for mock data
const MOCK_LATENCY_MS = 150;

function resolveMock(value) {
  return new Promise((resolve) =>
    setTimeout(() => resolve(value), MOCK_LATENCY_MS)
  );
}

// --------------------------------------------------
// Backend Flood Risk Prediction
// --------------------------------------------------

export async function predictFloodRisk({
  rainfall,
  rainfall_intensity,
  water_level,
  forecast_rainfall,
}) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      rainfall,
      rainfall_intensity,
      water_level,
      forecast_rainfall,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Failed to predict flood risk");
  }

  return data;
}

export async function getBackendForecast() {
  const response = await fetch(`${API_BASE_URL}/forecast`);

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Failed to load flood forecast");
  }

  return data;
}

// --------------------------------------------------
// Mock Dashboard Data
// --------------------------------------------------

export async function getSystemInfo() {
  return resolveMock(SYSTEM_INFO);
}

export async function getForecastTimeline() {
  return resolveMock(FORECAST_TIMELINE);
}

export async function getRainfallHistory(
  locationId = "L001"
) {
  const response = await fetch(
    `${API_BASE_URL}/rainfall/history?location_id=${locationId}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error ||
      "Failed to load rainfall history"
    );
  }

  return data.history;
}
export async function getAlerts() {
  return resolveMock(ALERTS);
}

export async function getRiskZones() {
  return resolveMock(RISK_ZONES);
}

export async function getLastUpdated() {
  return resolveMock(LAST_UPDATED);
}

export async function analyseFloodConditions(data) {
  const response = await fetch(`${API_BASE_URL}/analyse`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.error || "Failed to analyse flood conditions");
  }

  return result;
}

// --------------------------------------------------
// Backend GIS Location Risk Data
// --------------------------------------------------

export async function getLocationsRisk(
  forecastMinutes = 0
) {
  const response = await fetch(
    `${API_BASE_URL}/locations/risk?forecast_minutes=${forecastMinutes}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Failed to load location risks"
    );
  }

  return data.locations;
}

// --------------------------------------------------
// Backend Safe Routing
// --------------------------------------------------

export async function getSafeRoute(
  startId,
  endId
) {
  const response = await fetch(
    `${API_BASE_URL}/routing?start_id=${startId}&end_id=${endId}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Failed to generate safe route"
    );
  }

  return data;
}