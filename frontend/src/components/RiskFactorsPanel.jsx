import { useState } from "react";
import { useAnimatedNumber } from "../hooks/useAnimatedNumber";
import { formatNumber, formatPercent, isValidNumber } from "../utils/formatValue";
import "./RiskFactorsPanel.css";

function AnimatedStat({ value, decimals = 0, suffix = "" }) {
  const safe = isValidNumber(value) ? Number(value) : 0;
  const animated = useAnimatedNumber(safe);
  if (!isValidNumber(value)) return <>N/A</>;
  return <>{formatNumber(animated, { decimals, suffix })}</>;
}

function drainageStatus(pct) {
  if (pct === null) return { label: "N/A", colorVar: "--color-text-muted" };
  if (pct >= 100) return { label: "Capacity Exceeded", colorVar: "--color-risk-critical" };
  if (pct >= 90) return { label: "Near Capacity", colorVar: "--color-risk-critical" };
  if (pct >= 60) return { label: "Elevated Load", colorVar: "--color-risk-high" };
  if (pct >= 30) return { label: "Moderate Load", colorVar: "--color-risk-moderate" };
  return { label: "Normal", colorVar: "--color-risk-low" };
}

const TREND_ARROW = { Rising: "▲", Falling: "▼", Stable: "▬", Initial: "•" };

function TrendTag({ trend }) {
  if (!trend || !TREND_ARROW[trend]) return null;
  const colorVar =
    trend === "Rising" ? "--color-risk-high" : trend === "Falling" ? "--color-risk-low" : "--color-text-muted";
  return (
    <span className="factor-card__trend" style={{ color: `var(${colorVar})` }}>
      {TREND_ARROW[trend]} {trend}
    </span>
  );
}

const DETAILS = {
  "Rainfall": "Forecast rainfall intensity at this location and forecast time, from the backend's nowcast model.",
  "Surface Runoff": "Modelled rainwater draining off impervious surfaces rather than infiltrating, based on imperviousness, slope and soil saturation.",
  "Drainage Capacity Used": "Surface runoff as a share of the location's effective drainage capacity (design capacity reduced for years since maintenance).",
  "Excess Water": "Surface runoff exceeding effective drainage capacity — the modelled volume the drainage system cannot currently handle.",
  "Channel Fill Level": "Current water level as a fraction of the monitored drainage channel's capacity, smoothed from the latest observation.",
  "Soil Saturation": "Current estimated proportion of the soil profile already holding water at this location.",
};

export default function RiskFactorsPanel({ selectedForecast, analysis, location }) {
  console.log("Elevation:", location?.elevation);
  console.log("Slope:", location?.slope);
  console.log("Imperviousness:", location?.imperviousness);

  const [expanded, setExpanded] = useState(null);
  if (!selectedForecast) {
    return (
      <section className="panel" aria-labelledby="risk-factors-heading">
        <div className="panel-header">
          <h2 id="risk-factors-heading">Flood-Risk Contributing Factors</h2>
        </div>
        <div className="panel-body">
          <p className="factors-unavailable">Flood-risk factor data is currently unavailable for this location.</p>
        </div>
      </section>
    );
  }

  function toggle(label) {
    setExpanded((current) => (current === label ? null : label));
  }

  const drainagePct = isValidNumber(selectedForecast.drainage_capacity_used)
    ? selectedForecast.drainage_capacity_used * 100
    : null;
  const drainage = drainageStatus(drainagePct);

  const forecastFactors = [
    { label: "Rainfall", value: selectedForecast.rainfall, decimals: 0, unit: "mm/hr" },
    { label: "Surface Runoff", value: selectedForecast.surface_runoff, decimals: 1, unit: "mm/hr equiv." },
    { label: "Excess Water", value: selectedForecast.excess_water, decimals: 1, unit: "mm/hr equiv." },
  ];

  return (
    <section className="panel" aria-labelledby="risk-factors-heading">
      <div className="panel-header">
        <h2 id="risk-factors-heading">Flood-Risk Contributing Factors</h2>
        <span className="eyebrow">Tap a factor for detail</span>
      </div>

      <div className="factors-subheading">
        <span className="eyebrow">Forecast Conditions — at selected time</span>
      </div>
      <div className="panel-body factors-grid">
        {forecastFactors.map((f) => {
          const isOpen = expanded === f.label;
          return (
            <button
              type="button"
              key={f.label}
              className={`factor-card ${isOpen ? "factor-card--open" : ""}`}
              onClick={() => toggle(f.label)}
              aria-expanded={isOpen}
            >
              <span className="eyebrow">{f.label}</span>
              <div className="factor-card__value">
                <span className="mono factor-card__number">
                  <AnimatedStat value={f.value} decimals={f.decimals} />
                </span>
                <span className="factor-card__unit">{isValidNumber(f.value) ? f.unit : ""}</span>
              </div>
              <p className="factor-card__note">{isOpen ? DETAILS[f.label] : "Tap for detail"}</p>
            </button>
          );
        })}

        <button
          type="button"
          className={`factor-card ${expanded === "Drainage Capacity Used" ? "factor-card--open" : ""}`}
          onClick={() => toggle("Drainage Capacity Used")}
          aria-expanded={expanded === "Drainage Capacity Used"}
        >
          <span className="eyebrow">Drainage Capacity Used</span>
          <div className="factor-card__value">
            <span className="mono factor-card__number">
              {drainagePct === null ? "N/A" : <AnimatedStat value={drainagePct} decimals={0} />}
            </span>
            <span className="factor-card__unit">{drainagePct === null ? "" : "%"}</span>
          </div>
          {drainagePct !== null && (
            <div
              className="factor-card__bar"
              role="img"
              aria-label={`Drainage capacity used ${drainagePct.toFixed(0)} percent`}
            >
              <div
                className="factor-card__bar-fill"
                style={{
                  width: `${Math.min(drainagePct, 100)}%`,
                  background: `var(${drainage.colorVar})`,
                }}
              />
            </div>
          )}
          <p className="factor-card__note" style={{ color: `var(${drainage.colorVar})`, fontWeight: 600 }}>
            {expanded === "Drainage Capacity Used" ? DETAILS["Drainage Capacity Used"] : drainage.label}
          </p>
        </button>
      </div>

      <div className="factors-subheading">
        <span className="eyebrow">Current Observed Conditions — not forecast by the model</span>
      </div>
      <div className="panel-body factors-grid">
        <button
          type="button"
          className={`factor-card ${expanded === "Channel Fill Level" ? "factor-card--open" : ""}`}
          onClick={() => toggle("Channel Fill Level")}
          aria-expanded={expanded === "Channel Fill Level"}
        >
          <span className="eyebrow">Channel Fill Level</span>
          <div className="factor-card__value">
            <span className="mono factor-card__number">
              {formatPercent(analysis?.water_level_smoothed, 0)}
            </span>
          </div>
          <TrendTag trend={analysis?.water_level_trend} />
          <p className="factor-card__note">
            {expanded === "Channel Fill Level" ? DETAILS["Channel Fill Level"] : "Fraction of monitored channel capacity currently full"}
          </p>
        </button>

        <button
          type="button"
          className={`factor-card ${expanded === "Soil Saturation" ? "factor-card--open" : ""}`}
          onClick={() => toggle("Soil Saturation")}
          aria-expanded={expanded === "Soil Saturation"}
        >
          <span className="eyebrow">Soil Saturation</span>
          <div className="factor-card__value">
            <span className="mono factor-card__number">
              {formatPercent(analysis?.soil_saturation_smoothed, 0)}
            </span>
          </div>
          <TrendTag trend={analysis?.soil_saturation_trend} />
          <p className="factor-card__note">
            {expanded === "Soil Saturation" ? DETAILS["Soil Saturation"] : "Ground infiltration capacity remaining is limited"}
          </p>
        </button>

        {location && (
          <div className="factor-card factor-card--static">
            <span className="eyebrow">Site Characteristics</span>
            <div className="factor-card__static-row">
              <span>Elevation</span>
              <span className="mono">{formatNumber(location.elevation, { decimals: 1, suffix: " m" })}</span>
            </div>
            <div className="factor-card__static-row">
              <span>Slope</span>
              <span className="mono">{formatNumber(location.slope, { decimals: 1, suffix: "°" })}</span>
            </div>
            <div className="factor-card__static-row">
              <span>Imperviousness</span>
              <span className="mono">{formatPercent(location.imperviousness, 0)}</span>
            </div>
            <p className="factor-card__note">Static site data — does not change with forecast time</p>
          </div>
        )}
      </div>
    </section>
  );
}
