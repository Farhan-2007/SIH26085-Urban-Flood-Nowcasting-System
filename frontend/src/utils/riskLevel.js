// The backend has two risk-classification code paths that don't use the
// same label vocabulary:
//   - backend/flood_engine/risk_calculator.py (used by POST /api/predict)
//     returns "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
//   - backend/predictor.py RiskAggregator._classify (used by the forecast
//     inside POST /api/analyse and GET /api/forecast) returns
//     "Low" | "Moderate" | "High" | "Critical"
//
// The dashboard is built around /api/analyse's forecast, so this module
// normalizes whatever string that endpoint returns into one consistent
// UPPERCASE vocabulary for display. It does NOT recompute the risk level
// from the score — the backend already decided that; this only maps its
// label onto consistent styling.
const LABEL_MAP = {
  low: "LOW",
  medium: "MODERATE",
  moderate: "MODERATE",
  high: "HIGH",
  critical: "CRITICAL",
};

export function normalizeRiskLevel(rawLevel) {
  if (!rawLevel || typeof rawLevel !== "string") return null;
  return LABEL_MAP[rawLevel.trim().toLowerCase()] || null;
}

// Fallback only: if a numeric score is available but no level string was
// returned, classify it using the exact thresholds already defined in
// backend/predictor.py's RiskAggregator._classify (Low < 25, Moderate < 50,
// High < 75, else Critical) — not a new scale invented for the frontend.
export function scoreToRiskLevel(score) {
  if (typeof score !== "number" || Number.isNaN(score)) return null;
  if (score < 25) return "LOW";
  if (score < 50) return "MODERATE";
  if (score < 75) return "HIGH";
  return "CRITICAL";
}

export const RISK_LEVEL_META = {
  LOW: {
    label: "LOW",
    colorVar: "--color-risk-low",
    description: "Conditions are within normal operating range.",
  },
  MODERATE: {
    label: "MODERATE",
    colorVar: "--color-risk-moderate",
    description: "Elevated conditions warrant continued monitoring.",
  },
  HIGH: {
    label: "HIGH",
    colorVar: "--color-risk-high",
    description: "Significant flood risk. Precautionary action advised.",
  },
  CRITICAL: {
    label: "CRITICAL",
    colorVar: "--color-risk-critical",
    description: "Severe flood risk. Immediate response measures advised.",
  },
};

export function getRiskMeta(rawLevel, score) {
  const level = normalizeRiskLevel(rawLevel) || scoreToRiskLevel(score);
  if (!level) return null;
  return { level, ...RISK_LEVEL_META[level] };
}
