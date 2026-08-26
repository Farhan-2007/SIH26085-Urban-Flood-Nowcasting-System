// Converts a 0–100 flood-risk score into one of four risk levels.
// Thresholds are centralized here so they can be tuned without touching
// any UI component, and so the backend can eventually own this scale.
export const RISK_THRESHOLDS = {
  LOW: { max: 25 },
  MODERATE: { max: 50 },
  HIGH: { max: 75 },
  CRITICAL: { max: 100 },
};

export function getRiskLevel(score) {
  if (score <= RISK_THRESHOLDS.LOW.max) return "LOW";
  if (score <= RISK_THRESHOLDS.MODERATE.max) return "MODERATE";
  if (score <= RISK_THRESHOLDS.HIGH.max) return "HIGH";
  return "CRITICAL";
}

// Semantic colour tokens per risk level, referencing the CSS custom
// properties defined in index.css so styling stays in one place.
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

export function getRiskMeta(score) {
  const level = getRiskLevel(score);
  return { level, ...RISK_LEVEL_META[level] };
}
