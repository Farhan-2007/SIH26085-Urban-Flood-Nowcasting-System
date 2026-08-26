// Centralized mock data for the Urban Flood Nowcasting Dashboard.
//
// This file intentionally mirrors the shape of the responses that the
// backend team's API is expected to return (see src/services/api.js).
// When the real endpoints are available, only api.js needs to change —
// UI components should keep consuming the same data shapes defined here.

export const SYSTEM_INFO = {
  systemName: "Urban Flood Nowcasting System",
  subtitle: "Drainage and Rainfall Coupling",
  ministry: "Ministry of Earth Sciences, Government of India",
  problemStatementId: "SIH26085",
  problemStatement: "Street-level / urban flood-risk prediction and early warning",
  forecastHorizon: "0–3 hours",
  keyInputs: "Rainfall, terrain / surface runoff, drainage capacity",
  dataStatus: "Prototype Data (Mock)",
  monitoredZone: "Zone 4 — Ward 17, Central Drainage Basin",
};

// Nowcast timeline: NOW, +1hr, +2hr, +3hr
// Each entry carries every value that changes with forecast time so the
// timeline component can drive the whole dashboard from one selection.
export const FORECAST_TIMELINE = [
  {
    id: "now",
    label: "NOW",
    timeOffsetHours: 0,
    riskScore: 58,
    rainfallIntensity: 52, // mm/hr
    recentRainfall: 38, // mm, last 3 hours
    forecastRainfall: 55, // mm, forecast rainfall
    waterLevel: 1.1, // metres
    drainageCapacityUsed: 48, // %
    surfaceRunoff: "MEDIUM",
    soilSaturation: 68, // %
    forecastNote: "Rainfall is intensifying and drainage load is rising across the monitored zone.",
  },
  {
    id: "+1h",
    label: "+1 HR",
    timeOffsetHours: 1,
    riskScore: 74,
    rainfallIntensity: 70,
    recentRainfall: 50,
    forecastRainfall: 72, 
    waterLevel: 1.5,
    drainageCapacityUsed: 66,
    surfaceRunoff: "High",
    soilSaturation: 80,
    forecastNote: "Drainage load is approaching capacity as rainfall intensity nears its peak.",
  },
  {
    id: "+2h",
    label: "+2 HR",
    timeOffsetHours: 2,
    riskScore: 91,
    rainfallIntensity: 86,
    recentRainfall: 66,
    forecastRainfall: 88,
    waterLevel: 1.9,
    drainageCapacityUsed: 88,
    surfaceRunoff: "Very High",
    soilSaturation: 93,
    forecastNote: "Peak rainfall intensity reached. Drainage capacity is exceeded in low-lying areas.",
  },
  {
    id: "+3h",
    label: "+3 HR",
    timeOffsetHours: 3,
    riskScore: 47,
    rainfallIntensity: 22,
    recentRainfall: 70,
    forecastRainfall: 30, 
    waterLevel: 1.5,
    drainageCapacityUsed: 55,
    surfaceRunoff: "MEDIUM",
    soilSaturation: 85,
    forecastNote: "Rainfall is easing and water levels are receding, though the ground remains saturated.",
  },
];

// Rainfall time series for the trend chart (last 6 hours, mm/hr).
export const RAINFALL_HISTORY = [
  { time: "06:00", intensity: 12 },
  { time: "07:00", intensity: 18 },
  { time: "08:00", intensity: 34 },
  { time: "09:00", intensity: 41 },
  { time: "10:00", intensity: 58 },
  { time: "11:00", intensity: 65 },
  { time: "12:00", intensity: 72 },
];

export const ALERTS = [
  {
    id: "AL-1042",
    severity: "HIGH",
    title: "HIGH FLOOD RISK",
    message:
      "Heavy rainfall combined with reduced drainage capacity may result in localized flooding.",
    zone: "Zone 4 — Ward 17",
    time: "12:04 IST",
  },
  {
    id: "AL-1041",
    severity: "MEDIUM",
    title: "RAINFALL WARNING",
    message: "High-intensity rainfall expected to continue over the next hour.",
    zone: "Zone 4 — Ward 17",
    time: "11:40 IST",
  },
  {
    id: "AL-1039",
    severity: "MEDIUM",
    title: "DRAINAGE ALERT",
    message: "Drainage capacity utilisation is forecast to exceed 80% of rated threshold within two hours.",
    zone: "Sector 12 stormwater line",
    time: "11:22 IST",
  },
];

// Simplified geographic risk-zone data for the map placeholder / future
// GIS integration. Coordinates are relative (0–100) percentage positions
// within the map viewport, not real-world GPS coordinates.
export const RISK_ZONES = [
  { id: "z1", name: "Ward 17 — Central Basin", x: 46, y: 42, level: "CRITICAL", riskScore: 89 },
  { id: "z2", name: "Sector 12 — Stormwater Line", x: 62, y: 30, level: "HIGH", riskScore: 78 },
  { id: "z3", name: "Old Town Low-Lying Belt", x: 30, y: 58, level: "HIGH", riskScore: 74 },
  { id: "z4", name: "Riverside Colony", x: 70, y: 65, level: "MEDIUM", riskScore: 48 },
  { id: "z5", name: "North Ridge Residential", x: 55, y: 18, level: "LOW", riskScore: 18 },
  { id: "z6", name: "East Industrial Belt", x: 80, y: 45, level: "MEDIUM", riskScore: 42 },
];

export const LAST_UPDATED = "2026-08-26T12:05:00+05:30";
