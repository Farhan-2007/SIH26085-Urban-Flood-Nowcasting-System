// Data access layer for the Urban Flood Nowcasting Dashboard.
//
// UI components access dashboard data through the functions exported
// from this file.
//
// Flood-risk prediction, GIS risk data and safe routing
// are connected to the Flask backend.

import {
  SYSTEM_INFO,
  FORECAST_TIMELINE,
  ALERTS,
  RISK_ZONES,
  LAST_UPDATED,
} from "../data/mockData";


// ============================================================
// FLASK BACKEND API
// ============================================================

const API_BASE_URL =
  "http://127.0.0.1:5000/api";


// ============================================================
// MOCK DATA LATENCY
// ============================================================

const MOCK_LATENCY_MS = 150;


function resolveMock(value) {

  return new Promise(
    (resolve) =>

      setTimeout(
        () => resolve(value),
        MOCK_LATENCY_MS
      )

  );

}


// ============================================================
// BACKEND FLOOD RISK PREDICTION
// ============================================================

export async function predictFloodRisk({

  rainfall,
  rainfall_intensity,
  water_level,
  forecast_rainfall,

}) {

  const response = await fetch(

    `${API_BASE_URL}/predict`,

    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json",

      },

      body: JSON.stringify({

        rainfall,
        rainfall_intensity,
        water_level,
        forecast_rainfall,

      }),

    }

  );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(

      data.error ||
      "Failed to predict flood risk"

    );

  }


  return data;

}


// ============================================================
// BACKEND FORECAST
// ============================================================

export async function getBackendForecast() {

  const response =
    await fetch(
      `${API_BASE_URL}/forecast`
    );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(

      data.error ||
      "Failed to load flood forecast"

    );

  }


  return data;

}


// ============================================================
// SYSTEM INFORMATION
// ============================================================

export async function getSystemInfo() {

  return resolveMock(
    SYSTEM_INFO
  );

}


// ============================================================
// FORECAST TIMELINE
// ============================================================

export async function getForecastTimeline() {

  return resolveMock(
    FORECAST_TIMELINE
  );

}


// ============================================================
// RAINFALL HISTORY
// ============================================================

export async function getRainfallHistory(
  locationId = "L001"
) {

  const response =
    await fetch(

      `${API_BASE_URL}/rainfall/history?location_id=${locationId}`

    );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(

      data.error ||
      "Failed to load rainfall history"

    );

  }


  return data.history;

}


// ============================================================
// ALERTS
// ============================================================

export async function getAlerts() {

  return resolveMock(
    ALERTS
  );

}


// ============================================================
// RISK ZONES
// ============================================================

export async function getRiskZones() {

  return resolveMock(
    RISK_ZONES
  );

}


// ============================================================
// LAST UPDATED TIME
// ============================================================

export async function getLastUpdated() {

  return resolveMock(
    LAST_UPDATED
  );

}


// ============================================================
// BACKEND PREDICTOR–ANALYSER
// ============================================================

export async function analyseFloodConditions(
  data
) {

  const response =
    await fetch(

      `${API_BASE_URL}/analyse`,

      {

        method: "POST",

        headers: {

          "Content-Type":
            "application/json",

        },

        body:
          JSON.stringify(data),

      }

    );


  const result =
    await response.json();


  if (!response.ok) {

    throw new Error(

      result.error ||
      "Failed to analyse flood conditions"

    );

  }


  return result;

}


// ============================================================
// GIS LOCATION RISK DATA
//
// Supports:
// 0, 30, 60, 120 and 180 minute forecasts
// ============================================================

export async function getLocationsRisk(
  forecastMinutes = 0
) {

  const response =
    await fetch(

      `${API_BASE_URL}/locations/risk?forecast_minutes=${forecastMinutes}`

    );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(

      data.error ||
      "Failed to load location risks"

    );

  }


  return data.locations;

}


// ============================================================
// SAFE ROUTING
//
// Dynamically changes according to:
//
// - Start location
// - Destination
// - Forecast timeline
// ============================================================

export async function getSafeRoute(

  startId,
  endId,
  forecastMinutes = 0

) {

  const response =
    await fetch(

      `${API_BASE_URL}/routing?start_id=${startId}&end_id=${endId}&forecast_minutes=${forecastMinutes}`

    );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(

      data.error ||
      "Failed to generate safe route"

    );

  }


  return data;

}