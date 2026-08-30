import "./LocationSelector.css";

export default function LocationSelector({ locations, locationId, onChange, selectedLocation }) {
  return (
    <div className="location-selector">
      <div className="location-selector__control">
        <label htmlFor="location-select" className="eyebrow">
          Location
        </label>
        <select
          id="location-select"
          className="location-selector__select"
          value={locationId}
          onChange={(e) => onChange(e.target.value)}
        >
          {locations.map((loc) => (
            <option key={loc.locationId} value={loc.locationId}>
              {loc.name}
            </option>
          ))}
        </select>
      </div>
      {selectedLocation && (
        <span className="location-selector__coords mono">
          {selectedLocation.latitude.toFixed(4)}, {selectedLocation.longitude.toFixed(4)}
        </span>
      )}
    </div>
  );
}
