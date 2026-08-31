import { useEffect, useRef, useState } from "react";
import RiskBadge from "./RiskBadge";
import {
  normalizeRiskLevel,
  scoreToRiskLevel,
} from "../utils/riskLevel";
import "./ForecastTimeline.css";

const AUTOPLAY_INTERVAL_MS = 2200;

export default function ForecastTimeline({
  forecast = [],
  selectedStep = 0,
  onSelectStep,
}) {
  const [playing, setPlaying] = useState(true);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!playing || !forecast.length) {
      return undefined;
    }

    intervalRef.current = setInterval(() => {
      onSelectStep((current) => {
        const next = current + 1;

        return next >= forecast.length
          ? 0
          : next;
      });
    }, AUTOPLAY_INTERVAL_MS);

    return () => {
      clearInterval(intervalRef.current);
    };
  }, [
    playing,
    forecast.length,
    onSelectStep,
  ]);

  if (!forecast.length) {
    return (
      <section
        className="panel"
        aria-labelledby="timeline-heading"
      >
        <div className="panel-header">
          <h2 id="timeline-heading">
            0–3 Hour Flood Risk Forecast
          </h2>
        </div>

        <div className="panel-body">
          <p className="timeline__unavailable">
            Forecast data is currently unavailable
            for this location.
          </p>
        </div>
      </section>
    );
  }

  const currentStep =
    forecast[selectedStep] || forecast[0];

  const maxHours =
    forecast[forecast.length - 1]
      ?.timeOffsetHours || 1;

  function positionFor(hours) {
    return (hours / maxHours) * 100;
  }

  function handleKeyDown(e) {
    if (e.key === "ArrowRight") {
      setPlaying(false);

      onSelectStep((step) =>
        Math.min(
          step + 1,
          forecast.length - 1
        )
      );
    }

    if (e.key === "ArrowLeft") {
      setPlaying(false);

      onSelectStep((step) =>
        Math.max(step - 1, 0)
      );
    }
  }

  function selectStep(index) {
    setPlaying(false);
    onSelectStep(index);
  }

  return (
    <section
      className="panel"
      aria-labelledby="timeline-heading"
    >
      <div className="panel-header">
        <h2 id="timeline-heading">
          0–3 Hour Flood Risk Forecast
        </h2>

        <button
          type="button"
          className="timeline__play-toggle"
          onClick={() =>
            setPlaying((value) => !value)
          }
          aria-pressed={playing}
        >
          {playing
            ? "⏸ Pause"
            : "▶ Play Forecast"}
        </button>
      </div>

      <div className="panel-body">

        <div
          className="timeline"
          role="slider"
          tabIndex={0}
          aria-valuemin={0}
          aria-valuemax={
            forecast.length - 1
          }
          aria-valuenow={selectedStep}
          aria-valuetext={
            currentStep.label
          }
          aria-label="Forecast time selector"
          onKeyDown={handleKeyDown}
        >

          <div className="timeline__track">

            <div
              className="timeline__track-fill"
              style={{
                width: `${positionFor(
                  currentStep.timeOffsetHours
                )}%`,
              }}
            />

            {forecast.map(
              (step, index) => (
                <button
                  key={step.id}
                  type="button"
                  className={`timeline__node ${
                    index === selectedStep
                      ? "timeline__node--active"
                      : ""
                  }`}
                  style={{
                    left: `${positionFor(
                      step.timeOffsetHours
                    )}%`,
                  }}
                  onClick={() =>
                    selectStep(index)
                  }
                  aria-label={`Show forecast for ${step.label}`}
                  aria-pressed={
                    index === selectedStep
                  }
                >
                  <span className="timeline__node-dot" />
                </button>
              )
            )}

          </div>


          <div className="timeline__labels">

            {forecast.map(
              (step, index) => (
                <button
                  key={step.id}
                  type="button"
                  className={`timeline__label ${
                    index === selectedStep
                      ? "timeline__label--active"
                      : ""
                  }`}
                  style={{
                    left: `${positionFor(
                      step.timeOffsetHours
                    )}%`,
                  }}
                  onClick={() =>
                    selectStep(index)
                  }
                >
                  {step.label}
                </button>
              )
            )}

          </div>

        </div>


        <div className="timeline__summary">

          {forecast.map(
            (step, index) => {

              const level =
                normalizeRiskLevel(
                  step.riskLevel
                ) ||
                scoreToRiskLevel(
                  step.riskScore
                );

              return (
                <button
                  type="button"
                  key={step.id}
                  className={`timeline__summary-card ${
                    index === selectedStep
                      ? "timeline__summary-card--active"
                      : ""
                  }`}
                  onClick={() =>
                    selectStep(index)
                  }
                >

                  <span className="eyebrow">
                    {step.label}
                  </span>

                  <div className="timeline__summary-score mono">
                    {step.riskScore ?? "N/A"}
                  </div>

                  {level && (
                    <RiskBadge
                      level={level}
                      size="sm"
                    />
                  )}

                </button>
              );
            }
          )}

        </div>

      </div>
    </section>
  );
}