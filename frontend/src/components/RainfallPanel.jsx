import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceDot } from "recharts";
import { forecastMinutesLabel } from "../utils/forecastLabels";
import { isValidNumber } from "../utils/formatValue";
import "./RainfallPanel.css";

function CustomTooltip({ active, payload }) {
  if (!active || !payload || !payload.length) return null;
  const point = payload[0].payload;
  return (
    <div className="rainfall-tooltip">
      <span className="rainfall-tooltip__time mono">{forecastMinutesLabel(point.forecast_minutes)}</span>
      <span className="rainfall-tooltip__value mono">{point.rainfall} mm/hr</span>
    </div>
  );
}

export default function RainfallPanel({ forecast, selectedForecast }) {
  if (!selectedForecast || !Array.isArray(forecast) || forecast.length === 0) {
    return (
      <section className="panel" aria-labelledby="rainfall-heading">
        <div className="panel-header">
          <h2 id="rainfall-heading">Rainfall Conditions</h2>
        </div>
        <div className="panel-body">
          <p className="rainfall-panel__unavailable">Rainfall data is currently unavailable for this location.</p>
        </div>
      </section>
    );
  }

  const chartData = forecast.map((f) => ({
    ...f,
    label: forecastMinutesLabel(f.forecast_minutes),
  }));

  const current = forecast[0];

  return (
    <section className="panel" aria-labelledby="rainfall-heading">
      <div className="panel-header">
        <h2 id="rainfall-heading">Rainfall Conditions</h2>
      </div>
      <div className="panel-body rainfall-panel__body">
        <div className="rainfall-panel__readouts">
          <div className="rainfall-readout">
            <span className="eyebrow">
              {selectedForecast.forecast_minutes === 0 ? "Current Rainfall" : `Rainfall at ${forecastMinutesLabel(selectedForecast.forecast_minutes)}`}
            </span>
            <div>
              <span className="mono rainfall-readout__value">
                {isValidNumber(selectedForecast.rainfall) ? selectedForecast.rainfall : "N/A"}
              </span>
              <span className="rainfall-readout__unit"> mm/hr</span>
            </div>
          </div>
          {selectedForecast.forecast_minutes !== 0 && isValidNumber(current?.rainfall) && (
            <div className="rainfall-readout">
              <span className="eyebrow">Now (baseline)</span>
              <div>
                <span className="mono rainfall-readout__value">{current.rainfall}</span>
                <span className="rainfall-readout__unit"> mm/hr</span>
              </div>
            </div>
          )}
          <div className="rainfall-readout rainfall-readout--forecast">
            <span className="eyebrow">Model Status</span>
            <p className="rainfall-readout__forecast-text">
              {selectedForecast.prediction_status || "No status available"}
            </p>
          </div>
        </div>

        <div className="rainfall-panel__chart">
          <span className="eyebrow">Rainfall Forecast — Next 3 Hours (mm/hr)</span>
          <div className="rainfall-panel__chart-container">
            <ResponsiveContainer width="100%" height={160}>
              <LineChart data={chartData} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
                <CartesianGrid stroke="var(--color-border)" strokeDasharray="0" vertical={false} />
                <XAxis
                  dataKey="label"
                  tick={{ fontSize: 11, fill: "var(--color-text-muted)", fontFamily: "var(--font-mono)" }}
                  axisLine={{ stroke: "var(--color-border-strong)" }}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: "var(--color-text-muted)", fontFamily: "var(--font-mono)" }}
                  axisLine={false}
                  tickLine={false}
                  width={34}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="rainfall"
                  stroke="var(--color-blue-600)"
                  strokeWidth={2}
                  dot={{ r: 2.5, fill: "var(--color-blue-600)" }}
                  activeDot={{ r: 4 }}
                />
                <ReferenceDot
                  x={forecastMinutesLabel(selectedForecast.forecast_minutes)}
                  y={selectedForecast.rainfall}
                  r={5}
                  fill="var(--color-navy-900)"
                  stroke="#fff"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </section>
  );
}
