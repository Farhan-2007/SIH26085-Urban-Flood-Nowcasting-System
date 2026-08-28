export function getRiskColor(level) {
  const normalizedLevel =
    String(level || "").toUpperCase();

  switch (normalizedLevel) {
    // Low-risk values
    case "LOW":
    case "NORMAL":
      return "#22c55e";

    // Medium-risk values
    case "MEDIUM":
    case "WATCH":
      return "#eab308";

    // High-risk values
    case "HIGH":
    case "WARNING":
      return "#f97316";

    // Critical-risk values
    case "CRITICAL":
    case "SEVERE":
      return "#ef4444";

    default:
      return "#64748b";
  }
}