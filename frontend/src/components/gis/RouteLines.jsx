import { Polyline, Popup } from "react-leaflet";

export default function RouteLines({ routeData }) {

  if (!routeData) {
    return null;
  }


  // ==========================================================
  // REAL OSRM SAFE ROUTE
  // ==========================================================

  const osrmRoute =
    routeData.osrm_route;

  const geometry =
    osrmRoute?.geometry || [];


  const positions =
    geometry
      .filter(
        (coordinate) =>
          Array.isArray(coordinate) &&
          coordinate.length >= 2
      )
      .map(
        ([longitude, latitude]) => [
          latitude,
          longitude,
        ]
      );


  if (positions.length < 2) {
    return null;
  }


  return (
    <Polyline
      positions={positions}
      pathOptions={{
        color: "#2563eb",
        weight: 8,
        opacity: 0.95,
      }}
    >
      <Popup>

        <strong>
          🛣️ Safe Route
        </strong>

        <br />

        Distance:{" "}
        {osrmRoute.distance_km} km

        <br />

        Estimated time:{" "}
        {osrmRoute.duration_minutes} min

        <br />

        Flood Risk:{" "}
        {routeData.osrm_route_risk?.risk_level || "Low"}

        <br />

        Risk Score:{" "}
        {routeData.osrm_route_risk?.risk_score ?? 0}

      </Popup>

    </Polyline>
  );
}