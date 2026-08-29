import { CircleMarker, Popup } from "react-leaflet";
import { getRiskColor } from "./riskColor";
import { locations } from "./location";

function normalizeRiskLevel(level, score) {
  const normalized = String(level || "").toUpperCase();

  if (normalized === "MODERATE") return "MEDIUM";

  if (["LOW", "MEDIUM", "HIGH", "CRITICAL"].includes(normalized)) {
    return normalized;
  }

  if (score >= 80) return "CRITICAL";
  if (score >= 60) return "HIGH";
  if (score >= 30) return "MEDIUM";

  return "LOW";
}

export default function LocationMarkers({ forecastLabel }) {
  return (
    <>
      {locations.map((location) => {
        const riskScore = location.risk_score;
        const riskLevel = normalizeRiskLevel(
          location.risk_level,
          riskScore
        );
        const markerColor = getRiskColor(riskLevel);
        const isHotspot = riskScore >= 70;

        return (
          <CircleMarker
            key={location.location_id}
            center={[location.latitude, location.longitude]}
            radius={isHotspot ? 14 : 10}
            pathOptions={{
              color: markerColor,
              fillColor: markerColor,
              fillOpacity: 0.8,
              weight: isHotspot ? 4 : 2,
            }}
          >
            <Popup>
              <strong>{location.location_name}</strong>

              <br />

              Location ID: {location.location_id}

              <br />

              Forecast: {forecastLabel || "NOW"}

              <br />

              Risk: {riskLevel}

              <br />

              Risk Score: {riskScore}/100

              {isHotspot && (
                <>
                  <br />
                  <strong>🔥 FLOOD HOTSPOT</strong>
                </>
              )}
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}