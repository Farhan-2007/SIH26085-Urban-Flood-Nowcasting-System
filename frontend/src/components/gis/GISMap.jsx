import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import LocationMarkers from "./LocationMarkers";
import MapLegend from "./MapLegend";

export default function GISMap({
  zones,
  selected,
  analysis,
}) {
  /*
   * NOW:
   * Use the real-time Analyser risk.
   *
   * +1 / +2 / +3 HR:
   * Use the Predictor forecast risk.
   */
  const isNow = selected?.label === "NOW";

  const activeRiskScore =
    isNow && analysis
      ? analysis.flood_condition_index
      : selected?.riskScore;

  const activeRiskLevel =
    isNow && analysis
      ? analysis.condition
      : selected?.riskLevel?.toUpperCase();

  return (
    <MapContainer
      center={[19.076, 72.8777]}
      zoom={12}
      scrollWheelZoom={true}
      style={{
        height: "500px",
        width: "100%",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <LocationMarkers
        zones={zones}
        activeRiskScore={activeRiskScore}
        activeRiskLevel={activeRiskLevel}
        forecastLabel={selected?.label}
      />
    <MapLegend />
    </MapContainer>
  );
}