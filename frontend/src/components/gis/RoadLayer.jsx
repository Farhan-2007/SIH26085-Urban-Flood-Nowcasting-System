import { GeoJSON } from "react-leaflet";

export default function RoadLayer({ roads = [] }) {
  if (!roads.length) {
    return null;
  }

  const features = roads
    .filter(
      (road) =>
        Array.isArray(road.geometry) &&
        road.geometry.length >= 2
    )
    .map((road) => ({
      type: "Feature",
      properties: {
        road_id: road.road_id,
        road_name: road.road_name,
        risk_level: road.risk_level,
        distance_km: road.distance_km,
      },
      geometry: {
        type: "LineString",
        coordinates: road.geometry,
      },
    }));

  if (!features.length) {
    return null;
  }

  return (
    <GeoJSON
      data={{
        type: "FeatureCollection",
        features,
      }}
      style={(feature) => {
        const risk =
          feature?.properties?.risk_level;

        if (risk === "Critical" || risk === "High") {
          return {
            color: "#ef4444",
            weight: 4,
            opacity: 0.8,
          };
        }

        if (risk === "Moderate") {
          return {
            color: "#f59e0b",
            weight: 4,
            opacity: 0.8,
          };
        }

        return {
          color: "#22c55e",
          weight: 3,
          opacity: 0.7,
        };
      }}
    />
  );
}