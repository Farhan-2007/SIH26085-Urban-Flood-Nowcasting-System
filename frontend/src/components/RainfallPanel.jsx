import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import "./RainfallPanel.css";

function forecastLabel(intensity) {
  if (intensity >= 75) return "Heavy rainfall expected";
  if (intensity >= 40) return "Moderate to heavy rainfall expected";
  if (intensity >= 15) return "Light to moderate rainfall expected";
  return "Rainfall expected to remain light";
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="rainfall-tooltip">
      <span className="rainfall-tooltip__time mono">{label}</span>
      <span className="rainfall-tooltip__value mono">{payload[0].value} mm/hr</span>
    </div>
  );
}

export default function RainfallPanel({
  selected,
  history,
  analysis,
}) {
  if (!selected) return null;
  const isNow = selected.label === "NOW";

  const rainfallIntensity =
    isNow && analysis
      ? analysis.rainfall_smoothed
      : selected.rainfallIntensity;

  return (
    <section className="panel" aria-labelledby="rainfall-heading">
      <div className="panel-header">
        <h2 id="rainfall-heading">Rainfall Conditions</h2>
      </div>
      <div className="panel-body rainfall-panel__body">
        <div className="rainfall-panel__readouts">
          <div className="rainfall-readout">
            <span className="eyebrow">Current Rainfall</span>
            <div>
              <span className="mono rainfall-readout__value">{rainfallIntensity}</span>
              <span className="rainfall-readout__unit"> mm/hr</span>
            </div>
          </div>
          <div className="rainfall-readout">
            <span className="eyebrow">Recent (3 hr)</span>
            <div>
              <span className="mono rainfall-readout__value">{selected.recentRainfall}</span>
              <span className="rainfall-readout__unit"> mm</span>
            </div>
          </div>
          <div className="rainfall-readout rainfall-readout--forecast">
            <span className="eyebrow">Forecast</span>
            <p className="rainfall-readout__forecast-text">{forecastLabel(rainfallIntensity)}</p>
          </div>
        </div>

        <div className="rainfall-panel__chart">
          <span className="eyebrow">Rainfall Trend — Last 6 Hours (mm/hr)</span>
          <div className="rainfall-panel__chart-container">
            <ResponsiveContainer width="100%" height={160}>
              <LineChart data={history} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
                <CartesianGrid stroke="var(--color-border)" strokeDasharray="0" vertical={false} />
                <XAxis
                  dataKey="time"
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
                  dataKey="intensity"
                  stroke="var(--color-blue-600)"
                  strokeWidth={2}
                  dot={{ r: 2.5, fill: "var(--color-blue-600)" }}
                  activeDot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </section>
  );
}
