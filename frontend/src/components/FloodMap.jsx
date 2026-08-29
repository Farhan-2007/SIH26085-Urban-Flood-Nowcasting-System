import GISMap from "./gis/GISMap";
import "./FloodMap.css";

export default function FloodMap({
  locations,
  selected,
  selectedLocation,
  onSelectLocation,
}) {
  return (
    <section className="panel flood-map">
      <div className="panel-header">
        <h2>Geographic Flood-Risk Map</h2>

        <span className="eyebrow">
          {selectedLocation
            ? `Selected: ${selectedLocation.location_name} • ${selected?.label || "NOW"
            }`
            : "Select a location on the map"}
        </span>
      </div>

      <div className="panel-body">
        <GISMap
          locations={locations}
          selected={selected}
          selectedLocation={selectedLocation}
          onSelectLocation={onSelectLocation}
        />
      </div>
    </section>
  );
}