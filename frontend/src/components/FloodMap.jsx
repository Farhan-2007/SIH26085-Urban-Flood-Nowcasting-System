import { RISK_LEVEL_META } from "../utils/riskLevel";
import "./FloodMap.css";

// Normalizes the project's real lat/lon coordinates onto a 0-100 canvas.
// This is a schematic placeholder — not a geographic projection — kept
// isolated so Member 2's GIS component can be dropped in without any
// other part of the dashboard changing (it only needs locationId,
// latitude, longitude and a risk level/score per location).
function normalizePositions(locations) {
  const lats = locations.map((l) => l.latitude);
  const lons = locations.map((l) => l.longitude);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);
  const minLon = Math.min(...lons);
  const maxLon = Math.max(...lons);
  const pad = 12;

  return locations.map((loc) => {
    const xRatio = maxLon === minLon ? 0.5 : (loc.longitude - minLon) / (maxLon - minLon);
    const yRatio = maxLat === minLat ? 0.5 : (maxLat - loc.latitude) / (maxLat - minLat);
    return {
      ...loc,
      x: pad + xRatio * (100 - pad * 2),
      y: pad + yRatio * (100 - pad * 2),
    };
  });
}

export default function FloodMap({ locations, locationId, onSelectLocation, currentRiskLevel, forecastLabel }) {
  const positioned = normalizePositions(locations);

  return (
    <section className="panel flood-map" aria-labelledby="flood-map-heading">
      <div className="panel-header">
        <h2 id="flood-map-heading">Geographic Flood-Risk Map</h2>
        <span className="eyebrow">
          {forecastLabel && forecastLabel !== "NOW" ? `Risk shown for ${forecastLabel}` : "Click a location to switch"}
        </span>
      </div>
      <div className="panel-body flood-map__body">
        <div
          className="flood-map__canvas"
          role="img"
          aria-label="Map of monitored locations. Selected location is highlighted by its current risk level."
        >
          <svg viewBox="0 0 100 80" className="flood-map__basemap" preserveAspectRatio="none" aria-hidden="true">
            <rect x="0" y="0" width="100" height="80" fill="var(--color-surface-alt)" />
            <path
              d="M0,52 C20,48 35,60 50,55 C68,49 80,58 100,50"
              stroke="var(--color-blue-500)"
              strokeWidth="1.1"
              fill="none"
              opacity="0.4"
            />
          </svg>

          {positioned.map((loc) => {
            const isSelected = loc.locationId === locationId;
            const meta = isSelected && currentRiskLevel ? RISK_LEVEL_META[currentRiskLevel] : null;
            const colorVar = meta ? meta.colorVar : "--color-text-muted";
            return (
              <button
                key={loc.locationId}
                type="button"
                className={`flood-map__marker ${isSelected ? "flood-map__marker--active" : ""}`}
                style={{ left: `${loc.x}%`, top: `${loc.y}%`, borderColor: `var(${colorVar})` }}
                onClick={() => onSelectLocation(loc.locationId)}
                aria-pressed={isSelected}
                aria-label={`${loc.name}${isSelected && currentRiskLevel ? `, risk level ${currentRiskLevel}` : ""}`}
              >
                <span className="flood-map__marker-dot" style={{ background: `var(${colorVar})` }} />
              </button>
            );
          })}

          {positioned
            .filter((loc) => loc.locationId === locationId)
            .map((loc) => (
              <div key={loc.locationId} className="flood-map__tooltip" style={{ left: `${loc.x}%`, top: `${loc.y}%` }}>
                <span className="flood-map__tooltip-name">{loc.name}</span>
                {currentRiskLevel && (
                  <span className="mono flood-map__tooltip-level">{currentRiskLevel}</span>
                )}
              </div>
            ))}

          <span className="flood-map__notice">GIS module integration point — coordinates are real, layout is schematic</span>
        </div>

        <div className="flood-map__legend">
          <span className="eyebrow">Monitored Locations</span>
          {positioned.map((loc) => (
            <button
              key={loc.locationId}
              type="button"
              className={`flood-map__legend-item ${loc.locationId === locationId ? "flood-map__legend-item--active" : ""}`}
              onClick={() => onSelectLocation(loc.locationId)}
            >
              <span
                className="flood-map__legend-dot"
                style={{
                  background:
                    loc.locationId === locationId && currentRiskLevel
                      ? `var(${RISK_LEVEL_META[currentRiskLevel].colorVar})`
                      : "var(--color-text-muted)",
                }}
              />
              <span className="flood-map__legend-name">{loc.name}</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
