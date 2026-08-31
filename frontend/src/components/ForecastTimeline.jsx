import RiskBadge from "./RiskBadge";
import {
  normalizeRiskLevel,
  scoreToRiskLevel,
} from "../utils/riskLevel";

import "./ForecastTimeline.css";

export default function ForecastTimeline({
  forecast = [],
  selectedStep = 0,
  onSelectStep,
}) {
  // ==========================================================
  // NO AUTOPLAY
  // ==========================================================
  // Forecast changes ONLY when the user selects a time.
  // ==========================================================


  // ==========================================================
  // NO FORECAST DATA
  // ==========================================================

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


  // ==========================================================
  // CURRENT SELECTED FORECAST
  // ==========================================================

  const currentStep =
    forecast[selectedStep] ||
    forecast[0];


  // ==========================================================
  // MAX FORECAST HOURS
  // ==========================================================

  const maxHours =
    forecast[forecast.length - 1]
      ?.timeOffsetHours || 1;


  // ==========================================================
  // TIMELINE POSITION
  // ==========================================================

  function positionFor(hours) {
    return (hours / maxHours) * 100;
  }


  // ==========================================================
  // KEYBOARD NAVIGATION
  // ==========================================================

  function handleKeyDown(event) {

    if (event.key === "ArrowRight") {

      onSelectStep((step) =>
        Math.min(
          step + 1,
          forecast.length - 1
        )
      );

    }


    if (event.key === "ArrowLeft") {

      onSelectStep((step) =>
        Math.max(
          step - 1,
          0
        )
      );

    }

  }


  // ==========================================================
  // SELECT FORECAST STEP
  // ==========================================================

  function selectStep(index) {

    onSelectStep(index);

  }


  return (
    <section
      className="panel"
      aria-labelledby="timeline-heading"
    >

      {/* ================================================== */}
      {/* HEADER */}
      {/* ================================================== */}

      <div className="panel-header">

        <h2 id="timeline-heading">
          0–3 Hour Flood Risk Forecast
        </h2>

        <span className="eyebrow">
          Select forecast time
        </span>

      </div>


      <div className="panel-body">


        {/* ================================================== */}
        {/* TIMELINE */}
        {/* ================================================== */}

        <div
          className="timeline"
          role="slider"
          tabIndex={0}

          aria-valuemin={0}

          aria-valuemax={
            forecast.length - 1
          }

          aria-valuenow={
            selectedStep
          }

          aria-valuetext={
            currentStep.label
          }

          aria-label="Forecast time selector"

          onKeyDown={
            handleKeyDown
          }
        >


          {/* ================================================== */}
          {/* TRACK */}
          {/* ================================================== */}

          <div className="timeline__track">

            {/* CURRENT PROGRESS */}

            <div
              className="timeline__track-fill"

              style={{
                width: `${positionFor(
                  currentStep.timeOffsetHours
                )}%`,
              }}
            />


            {/* ================================================== */}
            {/* FORECAST NODES */}
            {/* ================================================== */}

            {forecast.map(
              (step, index) => (

                <button
                  key={step.id}

                  type="button"

                  className={
                    `timeline__node ${
                      index === selectedStep
                        ? "timeline__node--active"
                        : ""
                    }`
                  }

                  style={{
                    left: `${positionFor(
                      step.timeOffsetHours
                    )}%`,
                  }}

                  onClick={() =>
                    selectStep(index)
                  }

                  aria-label={
                    `Show forecast for ${step.label}`
                  }

                  aria-pressed={
                    index === selectedStep
                  }
                >

                  <span className="timeline__node-dot" />

                </button>

              )
            )}

          </div>


          {/* ================================================== */}
          {/* FORECAST TIME LABELS */}
          {/* ================================================== */}

          <div className="timeline__labels">

            {forecast.map(
              (step, index) => (

                <button
                  key={step.id}

                  type="button"

                  className={
                    `timeline__label ${
                      index === selectedStep
                        ? "timeline__label--active"
                        : ""
                    }`
                  }

                  style={{
                    left: `${positionFor(
                      step.timeOffsetHours
                    )}%`,
                  }}

                  onClick={() =>
                    selectStep(index)
                  }

                  aria-pressed={
                    index === selectedStep
                  }
                >

                  {step.label}

                </button>

              )
            )}

          </div>

        </div>


        {/* ================================================== */}
        {/* FORECAST SUMMARY CARDS */}
        {/* ================================================== */}

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

                  className={
                    `timeline__summary-card ${
                      index === selectedStep
                        ? "timeline__summary-card--active"
                        : ""
                    }`
                  }

                  onClick={() =>
                    selectStep(index)
                  }
                >

                  {/* TIME */}

                  <span className="eyebrow">
                    {step.label}
                  </span>


                  {/* RISK SCORE */}

                  <div className="timeline__summary-score mono">

                    {step.riskScore ??
                      "N/A"}

                  </div>


                  {/* RISK LEVEL */}

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