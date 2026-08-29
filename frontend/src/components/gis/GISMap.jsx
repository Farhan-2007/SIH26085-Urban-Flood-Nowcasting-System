import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import LocationMarkers from "./LocationMarkers";
import MapLegend from "./MapLegend";
import RouteLines from "./RouteLines";


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

      {/* Draw safer route and avoided roads */}
      <RouteLines
        locations={locations}
        roads={routeData?.roads || []}
        routeData={routeData}
      />

      {/* Flood risk location markers */}
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