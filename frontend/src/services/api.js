// Data access layer for the Urban Flood Nowcasting Dashboard.
//
// Every UI component reads dashboard data through the functions exported
// here rather than importing src/data/mockData.js directly. Today each
// function resolves mock data; once the backend team's REST endpoints are
// available, only the bodies below need to change (e.g. swap in a fetch()
// call to the real endpoint) — component code does not need to change.
//
// Expected future endpoints (not yet finalised):
//   GET /api/risk/current        -> current risk score, level, factors
//   GET /api/forecast            -> 0-3 hour nowcast timeline
//   GET /api/rainfall/history    -> recent rainfall time series
//   GET /api/alerts              -> active alerts / warnings
//   GET /api/map/risk-zones      -> geographic risk-zone data

import {
  SYSTEM_INFO,
  FORECAST_TIMELINE,
  RAINFALL_HISTORY,
  ALERTS,
  RISK_ZONES,
  LAST_UPDATED,
} from "../data/mockData";

// Simulates network latency so loading states behave realistically once
// real API calls are substituted in.
const MOCK_LATENCY_MS = 150;

function resolveMock(value) {
  return new Promise((resolve) => setTimeout(() => resolve(value), MOCK_LATENCY_MS));
}

export async function getSystemInfo() {
  return resolveMock(SYSTEM_INFO);
}

export async function getForecastTimeline() {
  return resolveMock(FORECAST_TIMELINE);
}

export async function getRainfallHistory() {
  return resolveMock(RAINFALL_HISTORY);
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
