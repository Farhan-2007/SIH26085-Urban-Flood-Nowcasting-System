import { useEffect, useRef, useState } from "react";
import RiskBadge from "./RiskBadge";
import { normalizeRiskLevel, scoreToRiskLevel } from "../utils/riskLevel";
import { forecastMinutesLabel } from "../utils/forecastLabels";
import "./ForecastTimeline.css";

const AUTOPLAY_INTERVAL_MS = 2200;

export default function ForecastTimeline({ forecast, selectedStep, onSelectStep }) {
  const [playing, setPlaying] = useState(false);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!playing) return undefined;
    intervalRef.current = setInterval(() => {
      onSelectStep((current) => {
        const next = current + 1;
        return next >= forecast.length ? 0 : next;
      });
    }, AUTOPLAY_INTERVAL_MS);
    return () => clearInterval(intervalRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, forecast.length]);

  if (!forecast.length) {
    return (
      <section className="panel" aria-labelledby="timeline-heading">
        <div className="panel-header">
          <h2 id="timeline-heading">0–3 Hour Flood Risk Forecast</h2>
        </div>
        <div className="panel-body">
          <p className="timeline__unavailable">Forecast data is currently unavailable for this location.</p>
        </div>
      </section>
    );
  }

  const maxMinutes = forecast[forecast.length - 1].forecast_minutes || 1;

  function positionFor(minutes) {
    return (minutes / maxMinutes) * 100;
  }

  function handleKeyDown(e) {
    if (e.key === "ArrowRight") {
      setPlaying(false);
      onSelectStep((s) => Math.min(s + 1, forecast.length - 1));
    } else if (e.key === "ArrowLeft") {
      setPlaying(false);
      onSelectStep((s) => Math.max(s - 1, 0));
    }
  }

  function selectStep(idx) {
    setPlaying(false);
    onSelectStep(idx);
  }

  return (
    <section className="panel" aria-labelledby="timeline-heading">
      <div className="panel-header">
        <h2 id="timeline-heading">0–3 Hour Flood Risk Forecast</h2>
        <button
          type="button"
          className="timeline__play-toggle"
          onClick={() => setPlaying((p) => !p)}
          aria-pressed={playing}
        >
          {playing ? "⏸ Pause" : "▶ Play Forecast"}
        </button>
      </div>
      <div className="panel-body">
        <div
          className="timeline"
          role="slider"
          tabIndex={0}
          aria-valuemin={0}
          aria-valuemax={forecast.length - 1}
          aria-valuenow={selectedStep}
          aria-valuetext={forecastMinutesLabel(forecast[selectedStep]?.forecast_minutes)}
          aria-label="Forecast time selector"
          onKeyDown={handleKeyDown}
        >
          <div className="timeline__track">
            <div
              className="timeline__track-fill"
              style={{ width: `${positionFor(forecast[selectedStep].forecast_minutes)}%` }}
            />
            {forecast.map((step, idx) => (
              <button
                key={step.forecast_minutes}
                type="button"
                className={`timeline__node ${idx === selectedStep ? "timeline__node--active" : ""}`}
                style={{ left: `${positionFor(step.forecast_minutes)}%` }}
                onClick={() => selectStep(idx)}
                aria-label={`Show forecast for ${forecastMinutesLabel(step.forecast_minutes)}`}
                aria-pressed={idx === selectedStep}
              >
                <span className="timeline__node-dot" />
              </button>
            ))}
          </div>
          <div className="timeline__labels">
            {forecast.map((step, idx) => (
              <button
                key={step.forecast_minutes}
                type="button"
                className={`timeline__label ${idx === selectedStep ? "timeline__label--active" : ""}`}
                style={{ left: `${positionFor(step.forecast_minutes)}%` }}
                onClick={() => selectStep(idx)}
              >
                {forecastMinutesLabel(step.forecast_minutes)}
              </button>
            ))}
          </div>
        </div>

        <div className="timeline__summary">
          {forecast.map((step, idx) => {
            const level = normalizeRiskLevel(step.risk_level) || scoreToRiskLevel(step.risk_score);
            return (
              <button
                type="button"
                key={step.forecast_minutes}
                className={`timeline__summary-card ${idx === selectedStep ? "timeline__summary-card--active" : ""}`}
                onClick={() => selectStep(idx)}
              >
                <span className="eyebrow">{forecastMinutesLabel(step.forecast_minutes)}</span>
                <div className="timeline__summary-score mono">{step.risk_score ?? "N/A"}</div>
                {level && <RiskBadge level={level} size="sm" />}
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
