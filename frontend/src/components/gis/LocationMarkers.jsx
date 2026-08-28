import { CircleMarker, Popup } from "react-leaflet";
import { getRiskColor } from "./riskColor";

function normalizeRiskLevel(level, score) {
  const normalized = String(level || "").toUpperCase();

  // Already valid GIS risk levels
  if (["LOW", "MEDIUM", "HIGH", "CRITICAL"].includes(normalized)) {
    return normalized;
  }

  // Convert Analyser conditions to GIS risk levels
  if (normalized === "NORMAL") return "LOW";
  if (normalized === "WATCH") return "MEDIUM";
  if (normalized === "WARNING") return "HIGH";
  if (normalized === "SEVERE") return "CRITICAL";

  // Fallback: determine level from risk score
  if (typeof score === "number") {
    if (score >= 80) return "CRITICAL";
    if (score >= 60) return "HIGH";
    if (score >= 30) return "MEDIUM";
    return "LOW";
  }

  return "LOW";
}

export default function LocationMarkers({
  zones,
  activeRiskScore,
  activeRiskLevel,
  forecastLabel,
}) {
  if (!zones || zones.length === 0) {
    return null;
  }

  return (
    <>
      {zones.map((zone) => {
        // Prototype conversion:
        // x/y are relative positions, not real GPS coordinates.
        const lat = 19.076 + (50 - zone.y) * 0.01;
        const lng = 72.8777 + (zone.x - 50) * 0.01;

        /*
         * Use selected NOW / forecast risk.
         */
        const riskScore =
          typeof activeRiskScore === "number"
            ? activeRiskScore
            : zone.riskScore;

        const riskLevel = normalizeRiskLevel(
          activeRiskLevel,
          riskScore
        );

        const markerColor = getRiskColor(riskLevel);

        return (
          <CircleMarker
            key={zone.id}
            center={[lat, lng]}
            radius={10}
            pathOptions={{
              color: markerColor,
              fillColor: markerColor,
              fillOpacity: 0.7,
            }}
          >
            <Popup>
              <strong>{zone.name}</strong>

              <br />

              Forecast: {forecastLabel || "NOW"}

              <br />

              Risk: {riskLevel}

              <br />

              Risk Score: {Number(riskScore).toFixed(1)}/100
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}