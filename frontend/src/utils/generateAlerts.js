import { normalizeRiskLevel } from "./riskLevel";

// Builds the alert list entirely from the /api/analyse response. Every
// alert here is conditional on an actual field crossing a real threshold
// already used elsewhere in the backend (e.g. drainage_stress >= 1 means
// backend/Analyser.py has already determined surface runoff exceeds the
// effective drainage capacity) — nothing is invented or always-on.
export function generateAlerts({ analysis, forecast, locationName }) {
  if (!analysis || !Array.isArray(forecast)) return [];

  const alerts = [];
  const now = analysis.timestamp || new Date().toISOString();
  const current = forecast[0];
  const currentLevel = current ? normalizeRiskLevel(current.risk_level) : null;

  if (analysis.lightning === true) {
    alerts.push({
      id: "lightning",
      severity: "HIGH",
      title: "LIGHTNING DETECTED",
      message: "Lightning activity reported at the monitored location. Exercise caution in open or elevated areas.",
      zone: locationName,
      time: now,
    });
  }

  if (typeof analysis.drainage_stress === "number" && analysis.drainage_stress >= 1) {
    alerts.push({
      id: "drainage-exceeded",
      severity: "CRITICAL",
      title: "DRAINAGE CAPACITY EXCEEDED",
      message: `Surface runoff has exceeded the effective drainage capacity at this location. Excess water: ${
        typeof analysis.excess_water === "number" ? analysis.excess_water.toFixed(1) : "N/A"
      } mm/hr equivalent.`,
      zone: locationName,
      time: now,
    });
  } else if (typeof analysis.drainage_stress === "number" && analysis.drainage_stress >= 0.8) {
    alerts.push({
      id: "drainage-elevated",
      severity: "HIGH",
      title: "DRAINAGE LOAD ELEVATED",
      message: `Drainage utilisation is at ${(analysis.drainage_stress * 100).toFixed(0)}% of effective capacity and approaching its limit.`,
      zone: locationName,
      time: now,
    });
  }

  if (currentLevel === "HIGH" || currentLevel === "CRITICAL") {
    alerts.push({
      id: "current-risk",
      severity: currentLevel,
      title: currentLevel === "CRITICAL" ? "CRITICAL FLOOD RISK" : "HIGH FLOOD RISK",
      message: `Current flood-risk score at this location is ${current.risk_score}/100, based on rainfall, runoff and drainage conditions.`,
      zone: locationName,
      time: now,
    });
  }

  const criticalForecastPoint = forecast.find((f) => normalizeRiskLevel(f.risk_level) === "CRITICAL");
  if (criticalForecastPoint && criticalForecastPoint.forecast_minutes !== current?.forecast_minutes) {
    alerts.push({
      id: "forecast-critical",
      severity: "CRITICAL",
      title: "CRITICAL RISK FORECAST AHEAD",
      message: `Flood risk is forecast to reach CRITICAL within ${criticalForecastPoint.forecast_minutes} minutes.`,
      zone: locationName,
      time: now,
    });
  }

  if (analysis.overall_trend === "Deteriorating") {
    alerts.push({
      id: "trend-deteriorating",
      severity: "MODERATE",
      title: "CONDITIONS DETERIORATING",
      message: "Rainfall, water level and soil saturation are trending upward together at this location.",
      zone: locationName,
      time: now,
    });
  }

  return alerts;
}
