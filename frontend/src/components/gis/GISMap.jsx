import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import LocationMarkers from "./LocationMarkers";
import MapLegend from "./MapLegend";

export default function GISMap({
  locations,
  selected,
  selectedLocation,
  onSelectLocation,
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

