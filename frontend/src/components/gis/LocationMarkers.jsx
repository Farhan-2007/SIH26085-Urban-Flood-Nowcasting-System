import { CircleMarker, Popup } from "react-leaflet";
import { getRiskColor } from "./riskColor";

export default function LocationMarkers({ zones }) {
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

        return (
          <CircleMarker
            key={zone.id}
            center={[lat, lng]}
            radius={10}
            pathOptions={{
              color: getRiskColor(zone.level),
              fillColor: getRiskColor(zone.level),
              fillOpacity: 0.7,
            }}
          >
            <Popup>
              <strong>{zone.name}</strong>
              <br />
              Risk: {zone.level}
              <br />
              Risk Score: {zone.riskScore}/100
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}
