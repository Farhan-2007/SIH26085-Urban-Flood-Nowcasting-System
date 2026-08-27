import { CircleMarker, Popup } from "react-leaflet";
import { mockFloodPoints } from "./mockGISData";
import { getRiskColor } from "./riskColor";

export default function LocationMarkers() {
  return (
    <>
      {mockFloodPoints.map((point) => (
        <CircleMarker
          key={point.id}
          center={[point.lat, point.lng]}
          radius={10}
          pathOptions={{
            color: getRiskColor(point.riskLevel),
            fillColor: getRiskColor(point.riskLevel),
            fillOpacity: 0.7,
          }}
        >
          <Popup>
            <strong>{point.name}</strong>
            <br />
            Risk: {point.riskLevel}
            <br />
            Risk Score: {point.riskScore}
            <br />
            Water Depth: {point.waterDepth} cm
          </Popup>
        </CircleMarker>
      ))}
    </>
  );
}