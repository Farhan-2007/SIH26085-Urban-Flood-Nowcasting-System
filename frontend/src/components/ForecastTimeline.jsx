import RiskBadge from "./RiskBadge";
import { getRiskLevel } from "../utils/riskLevel";
import "./ForecastTimeline.css";

export default function ForecastTimeline({
  timeline,
  selectedStep,
  onSelectStep,
}) {
  if (!timeline.length) return null;

  function handleKeyDown(e) {
    if (e.key === "ArrowRight") {
      onSelectStep(
        Math.min(selectedStep + 1, timeline.length - 1)
      );
    } else if (e.key === "ArrowLeft") {
      onSelectStep(
        Math.max(selectedStep - 1, 0)
      );
    }
  }

  const getPosition = (idx) => {
    if (timeline.length <= 1) return 0;

    return (idx / (timeline.length - 1)) * 100;
  };

  return (
    <section
      className="panel"
      aria-labelledby="timeline-heading"
    >
      <div className="panel-header">
        <h2 id="timeline-heading">
          0–3 Hour Flood Risk Forecast
        </h2>

        <span className="eyebrow">
          Nowcast Timeline
        </span>
      </div>

      <div className="panel-body">

        {/* Timeline */}
        <div
          className="timeline"
          role="slider"
          tabIndex={0}
          aria-valuemin={0}
          aria-valuemax={timeline.length - 1}
          aria-valuenow={selectedStep}
          aria-valuetext={timeline[selectedStep]?.label}
          aria-label="Forecast time selector"
          onKeyDown={handleKeyDown}
        >
          <div className="timeline__track">

            {/* Active progress */}
            <div
              className="timeline__track-fill"
              style={{
                width: `${getPosition(selectedStep)}%`,
              }}
            />

            {/* Timeline nodes */}
            {timeline.map((step, idx) => (
              <button
                key={step.id}
                type="button"
                className={`timeline__node ${
                  idx === selectedStep
                    ? "timeline__node--active"
                    : ""
                }`}
                style={{
                  left: `${getPosition(idx)}%`,
                }}
                onClick={() => onSelectStep(idx)}
                aria-label={`Show forecast for ${step.label}`}
                aria-pressed={idx === selectedStep}
              >
                <span className="timeline__node-dot" />
              </button>
            ))}
          </div>

          {/* Labels */}
          <div className="timeline__labels">
            {timeline.map((step, idx) => (
              <button
                key={step.id}
                type="button"
                className={`timeline__label ${
                  idx === selectedStep
                    ? "timeline__label--active"
                    : ""
                }`}
                style={{
                  left: `${getPosition(idx)}%`,
                }}
                onClick={() => onSelectStep(idx)}
              >
                {step.label}
              </button>
            ))}
          </div>
        </div>

        {/* Forecast summary cards */}
        <div className="timeline__summary">
          {timeline.map((step, idx) => (
            <button
              key={step.id}
              type="button"
              className={`timeline__summary-card ${
                idx === selectedStep
                  ? "timeline__summary-card--active"
                  : ""
              }`}
              onClick={() => onSelectStep(idx)}
              aria-label={`Select ${step.label} forecast`}
            >
              <span className="eyebrow">
                {step.label}
              </span>

              <div className="timeline__summary-score mono">
                {step.riskScore}
              </div>

              <RiskBadge
                level={getRiskLevel(step.riskScore)}
                size="sm"
              />
            </button>
          ))}
        </div>

      </div>
    </section>
  );
}