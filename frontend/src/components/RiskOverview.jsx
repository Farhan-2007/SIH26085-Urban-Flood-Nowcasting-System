import RiskGauge from "./RiskGauge";
import RiskBadge from "./RiskBadge";
import { getRiskMeta } from "../utils/riskLevel";
import "./RiskOverview.css";

export default function RiskOverview({ selected }) {
  if (!selected) return null;
  const meta = getRiskMeta(selected.riskScore);

  return (
    <section className="panel risk-overview" aria-labelledby="risk-overview-heading">
      <div className="panel-header">
        <h2 id="risk-overview-heading">Current Flood Risk</h2>
        <span className="eyebrow">{selected.label === "NOW" ? "Live Assessment" : `Forecast: ${selected.label}`}</span>
      </div>
      <div className="panel-body risk-overview__body">
        <RiskGauge score={selected.riskScore} level={meta.level} />

        <div className="risk-overview__details">
          <div className="risk-overview__level-row">
            <RiskBadge level={meta.level} size="lg" />
            <span className="risk-overview__status-label">Risk Status</span>
          </div>
          <p className="risk-overview__description">{meta.description}</p>
          <p className="risk-overview__note">{selected.forecastNote}</p>
        </div>
      </div>
    </section>
  );
}
