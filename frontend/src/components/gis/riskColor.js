export function getRiskColor(level) {
  switch (level) {
    case "LOW":
      return "#22c55e";

    case "MEDIUM":
      return "#eab308";

    case "HIGH":
      return "#f97316";

    case "CRITICAL":
      return "#ef4444";

    default:
      return "#64748b";
  }
}