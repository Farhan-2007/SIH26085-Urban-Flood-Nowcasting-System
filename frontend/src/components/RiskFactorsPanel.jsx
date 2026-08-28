import "./RiskFactorsPanel.css";

function drainageStatus(pct) {
  if (pct >= 80) {
    return {
      label: "Near Capacity",
      colorVar: "--color-risk-critical",
    };
  }

  if (pct >= 60) {
    return {
      label: "Elevated Load",
      colorVar: "--color-risk-high",
    };
  }

  if (pct >= 35) {
    return {
      label: "Moderate Load",
      colorVar: "--color-risk-moderate",
    };
  }

  return {
    label: "Normal",
    colorVar: "--color-risk-low",
  };
}

function runoffColorVar(level) {
  if (level === "Very High") return "--color-risk-critical";
  if (level === "High") return "--color-risk-high";
  if (level === "Moderate") return "--color-risk-moderate";

  return "--color-risk-low";
}

export default function RiskFactorsPanel({ selected, analysis }) {
  if (!selected) return null;

  /*
   * Use live analyser data only for NOW.
   * Forecast steps continue using Predictor data.
   */
  const isNow = selected.label === "NOW";

  const rainfallIntensity =
    isNow && analysis
      ? analysis.rainfall_smoothed
      : selected.rainfallIntensity;

  /*
   * Backend water level is currently a ratio between 0 and 1.
   * Convert it to percentage for dashboard display.
   */
  const waterLevel =
    isNow && analysis
      ? Math.round(analysis.water_level_smoothed * 100)
      : selected.waterLevel;

  const soilSaturation =
    isNow && analysis
      ? Math.round(analysis.soil_saturation_smoothed * 100)
      : selected.soilSaturation;

  const drainageCapacityUsed =
    isNow && analysis
      ? Math.round(analysis.drainage_stress * 100)
      : selected.drainageCapacityUsed;

  const surfaceRunoff =
    isNow && analysis
      ? analysis.surface_runoff
      : selected.surfaceRunoff;

  const drainage = drainageStatus(drainageCapacityUsed);

  const factors = [
    {
      label: "Rainfall Intensity",
      value: rainfallIntensity,
      unit: "mm/hr",
      note: isNow
        ? `Trend: ${analysis?.rainfall_trend || "Stable"}`
        : "Forecast rainfall intensity",
    },
    {
      label: "Water Level",
      value: waterLevel,
      unit: "%",
      note: isNow
        ? `Trend: ${analysis?.water_level_trend || "Stable"}`
        : "Predicted water level",
    },
    {
      label: "Soil Saturation",
      value: soilSaturation,
      unit: "%",
      note: isNow
        ? `Trend: ${analysis?.soil_saturation_trend || "Stable"}`
        : "Forecast soil saturation",
    },
  ];

  return (
    <section className="panel" aria-labelledby="risk-factors-heading">
      <div className="panel-header">
        <h2 id="risk-factors-heading">
          Flood-Risk Contributing Factors
        </h2>

        {isNow && analysis && (
          <span className="eyebrow">
            Real-time Analyser
          </span>
        )}
      </div>

      <div className="panel-body factors-grid">
        {factors.map((f) => (
          <div className="factor-card" key={f.label}>
            <span className="eyebrow">
              {f.label}
            </span>

            <div className="factor-card__value">
              <span className="mono factor-card__number">
                {f.value}
              </span>

              <span className="factor-card__unit">
                {f.unit}
              </span>
            </div>

            <p className="factor-card__note">
              {f.note}
            </p>
          </div>
        ))}

        <div className="factor-card">
          <span className="eyebrow">
            Drainage Capacity Used
          </span>

          <div className="factor-card__value">
            <span className="mono factor-card__number">
              {drainageCapacityUsed}
            </span>

            <span className="factor-card__unit">
              %
            </span>
          </div>

          <div
            className="factor-card__bar"
            role="img"
            aria-label={`Drainage capacity used ${drainageCapacityUsed} percent`}
          >
            <div
              className="factor-card__bar-fill"
              style={{
                width: `${Math.min(drainageCapacityUsed, 100)}%`,
                background: `var(${drainage.colorVar})`,
              }}
            />
          </div>

          <p
            className="factor-card__note"
            style={{
              color: `var(${drainage.colorVar})`,
              fontWeight: 600,
            }}
          >
            {drainage.label}
          </p>
        </div>

        <div className="factor-card">
          <span className="eyebrow">
            Surface Runoff
          </span>

          <div className="factor-card__value">
            <span className="mono factor-card__number">
              {typeof surfaceRunoff === "number"
                ? surfaceRunoff.toFixed(1)
                : surfaceRunoff}
            </span>

            {typeof surfaceRunoff === "number" && (
              <span className="factor-card__unit">
                units
              </span>
            )}
          </div>

          <p className="factor-card__note">
            {isNow && analysis
              ? "Calculated from rainfall, soil saturation and urban surface conditions"
              : "Runoff generated by impervious urban surfaces"}
          </p>
        </div>
      </div>
    </section>
  );
}