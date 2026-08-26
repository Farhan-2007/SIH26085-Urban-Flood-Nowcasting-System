import { useState } from "react";
import RiskBadge from "./RiskBadge";
import { RISK_LEVEL_META } from "../utils/riskLevel";
import "./FloodMap.css";

// Renders a labelled placeholder for the geographic flood-risk map.
// The component is intentionally isolated so the team's GIS
// implementation (e.g. Leaflet/Mapbox with real basemap tiles) can be
// substituted here without changing how the rest of the dashboard
// consumes risk-zone data (see src/services/api.js: getRiskZones).
export default function FloodMap({ zones }) {
  const [activeZone, setActiveZone] = useState(null);
  const zone = zones.find((z) => z.id === activeZone) || null;

  return (
    <section className="panel flood-map" aria-labelledby="flood-map-heading">
      <div className="panel-header">
        <h2 id="flood-map-heading">Geographic Flood-Risk Map</h2>
        <span className="eyebrow">Zone-Level Risk Overlay</span>
      </div>
      <div className="panel-body flood-map__body">
        <div className="flood-map__canvas" role="img" aria-label="Map of monitored urban zones showing flood risk levels">
          <svg viewBox="0 0 100 80" className="flood-map__basemap" preserveAspectRatio="none" aria-hidden="true">
            <rect x="0" y="0" width="100" height="80" fill="var(--color-surface-alt)" />
            {/* Schematic drainage / river line to ground the placeholder geographically */}
            <path d="M0,52 C20,48 35,60 50,55 C68,49 80,58 100,50" stroke="var(--color-blue-500)" strokeWidth="1.1" fill="none" opacity="0.55" />
            <path d="M18,0 L22,80" stroke="var(--color-border-strong)" strokeWidth="0.4" fill="none" />
            <path d="M0,30 L100,26" stroke="var(--color-border-strong)" strokeWidth="0.4" fill="none" />
            <path d="M62,0 L58,80" stroke="var(--color-border-strong)" strokeWidth="0.4" fill="none" />
          </svg>

          {zones.map((z) => {
            const meta = RISK_LEVEL_META[z.level];
            const isActive = z.id === activeZone;
            return (
              <button
                key={z.id}
                type="button"
                className={`flood-map__marker ${isActive ? "flood-map__marker--active" : ""}`}
                style={{ left: `${z.x}%`, top: `${z.y}%`, borderColor: `var(${meta.colorVar})` }}
                onClick={() => setActiveZone(isActive ? null : z.id)}
                aria-pressed={isActive}
                aria-label={`${z.name}, risk level ${z.level}, score ${z.riskScore}`}
              >
                <span className="flood-map__marker-dot" style={{ background: `var(${meta.colorVar})` }} />
              </button>
            );
          })}

          {zone && (
            <div
              className="flood-map__tooltip"
              style={{ left: `${zone.x}%`, top: `${zone.y}%` }}
            >
              <span className="flood-map__tooltip-name">{zone.name}</span>
              <div className="flood-map__tooltip-meta">
                <RiskBadge level={zone.level} size="sm" />
                <span className="mono">{zone.riskScore}/100</span>
              </div>
            </div>
          )}

          <span className="flood-map__notice">Placeholder geography — pending GIS module integration</span>
        </div>

        <div className="flood-map__legend">
          <span className="eyebrow">Zone Legend</span>
          {zones.map((z) => (
            <button
              key={z.id}
              type="button"
              className={`flood-map__legend-item ${z.id === activeZone ? "flood-map__legend-item--active" : ""}`}
              onClick={() => setActiveZone(z.id === activeZone ? null : z.id)}
            >
              <span
                className="flood-map__legend-dot"
                style={{ background: `var(${RISK_LEVEL_META[z.level].colorVar})` }}
              />
              <span className="flood-map__legend-name">{z.name}</span>
              <RiskBadge level={z.level} size="sm" />
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
