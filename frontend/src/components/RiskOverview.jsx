import RiskGauge from "./RiskGauge";
import RiskBadge from "./RiskBadge";
import { getRiskMeta } from "../utils/riskLevel";
import "./RiskOverview.css";

export default function RiskOverview({ selected, analysis }) {
  if (!selected) return null;

  const isNow = selected.label === "NOW";

  // Use real-time Analyser FCI for NOW
  const riskScore =
    isNow && analysis
      ? analysis.flood_condition_index
      : selected.riskScore;

  const meta = getRiskMeta(riskScore);

  const condition =
    isNow && analysis
      ? analysis.condition
      : null;

  const overallTrend =
    isNow && analysis
      ? analysis.overall_trend
      : null;

  return (
    <section
      className="panel risk-overview"
      aria-labelledby="risk-overview-heading"
    >
      <div className="panel-header">
        <h2 id="risk-overview-heading">
          Current Flood Risk
        </h2>

        <span className="eyebrow">
          {isNow
            ? "Real-time Assessment"
            : `Forecast: ${selected.label}`}
        </span>
      </div>

      <div className="panel-body risk-overview__body">
        <RiskGauge
          score={riskScore}
          level={meta.level}
        />

        <div className="risk-overview__details">
          <div className="risk-overview__level-row">
            <RiskBadge
              level={meta.level}
              size="lg"
            />

            <span className="risk-overview__status-label">
              Risk Status
            </span>
          </div>

          <p className="risk-overview__description">
            {meta.description}
          </p>

          {isNow && analysis && (
            <>
              <p className="risk-overview__analyser">
                <strong>Flood Condition:</strong>{" "}
                {condition}
              </p>

              <p className="risk-overview__analyser">
                <strong>Overall Trend:</strong>{" "}
                {overallTrend}
              </p>
            </>
          )}

          <p className="risk-overview__note">
            {selected.forecastNote}
          </p>
        </div>
      </div>
    </section>
  );
}