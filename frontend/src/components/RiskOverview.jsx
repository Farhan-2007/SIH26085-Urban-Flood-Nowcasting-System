import RiskGauge from "./RiskGauge";
import RiskBadge from "./RiskBadge";
import { getRiskMeta } from "../utils/riskLevel";
import { forecastMinutesLabel } from "../utils/forecastLabels";
import "./RiskOverview.css";

const TREND_META = {
  Deteriorating: { label: "Deteriorating", colorVar: "--color-risk-high" },
  Improving: { label: "Improving", colorVar: "--color-risk-low" },
  Stable: { label: "Stable", colorVar: "--color-info" },
};

export default function RiskOverview({ selectedForecast, analysis, locationName, lastUpdated }) {
  if (!selectedForecast) {
    return (
      <section className="panel risk-overview" aria-labelledby="risk-overview-heading">
        <div className="panel-header">
          <h2 id="risk-overview-heading">Current Flood Risk — {locationName || "Unknown Location"}</h2>
        </div>
        <div className="panel-body">
          <p className="risk-overview__unavailable">Unable to retrieve current flood-risk data for this location.</p>
        </div>
      </section>
    );
  }

  const meta = getRiskMeta(selectedForecast.risk_level, selectedForecast.risk_score);
  const trend = analysis?.overall_trend ? TREND_META[analysis.overall_trend] : null;
  const isNow = selectedForecast.forecast_minutes === 0;

  return (
    <section className="panel risk-overview" aria-labelledby="risk-overview-heading">
      <div className="panel-header">
        <h2 id="risk-overview-heading">Current Flood Risk — {locationName}</h2>
        <span className="eyebrow">
          {isNow ? "Live Assessment" : `Forecast: ${forecastMinutesLabel(selectedForecast.forecast_minutes)}`}
        </span>
      </div>
      <div className="panel-body risk-overview__body">
        {meta ? (
          <RiskGauge score={selectedForecast.risk_score} level={meta.level} />
        ) : (
          <div className="risk-overview__unavailable">Risk score unavailable</div>
        )}

        <div className="risk-overview__details">
          <div className="risk-overview__level-row">
            {meta && <RiskBadge level={meta.level} size="lg" />}
            <span className="risk-overview__status-label">Risk Status</span>
            {trend && isNow && (
              <span className="risk-overview__trend" style={{ color: `var(${trend.colorVar})` }}>
                Trend: {trend.label}
              </span>
            )}
          </div>
          {meta && <p className="risk-overview__description">{meta.description}</p>}
          {selectedForecast.prediction_status && !isNow && (
            <p className="risk-overview__note">
              Model indicates conditions are <strong>{selectedForecast.prediction_status.toLowerCase()}</strong> relative to the previous forecast point.
            </p>
          )}
          {lastUpdated && (
            <p className="risk-overview__updated mono">
              Last updated {lastUpdated.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false })} IST
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
