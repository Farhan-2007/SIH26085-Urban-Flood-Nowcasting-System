import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import LocationMarkers from "./LocationMarkers";
import MapLegend from "./MapLegend";
import RouteLines from "./RouteLines";
import RoadLayer from "./RoadLayer";

export default function GISMap({
  locations,
  selected,
  selectedLocation,
  onSelectLocation,
  routeData,
}) {
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

      <RoadLayer
        roads={routeData?.affected_roads || []}
      />

      {/* ONLY REAL SAFE ROUTE */}
      <RouteLines
        locations={locations}
        routeData={routeData}
      />

      <LocationMarkers
        locations={locations}
        forecastLabel={selected?.label}
        selectedLocation={selectedLocation}
        onSelectLocation={onSelectLocation}
      />

      <MapLegend />
    </MapContainer>
  );
}