import { RISK_LEVEL_META } from "../utils/riskLevel";
import "./RiskBadge.css";

// Renders a consistent, semantically-coloured label for a risk level.
// Accepts either a level string ("HIGH") directly, so it can be reused
// anywhere a risk level is displayed (overview, map legend, alerts).
export default function RiskBadge({ level, size = "md" }) {
  const meta = RISK_LEVEL_META[level];
  if (!meta) return null;

  return (
    <span
      className={`risk-badge risk-badge--${size}`}
      style={{
        color: `var(${meta.colorVar})`,
        borderColor: `var(${meta.colorVar})`,
      }}
    >
      {meta.label}
    </span>
  );
}
