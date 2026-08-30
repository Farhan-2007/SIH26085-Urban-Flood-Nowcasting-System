import "./AlertsPanel.css";

const SEVERITY_COLOR_VAR = {
  CRITICAL: "--color-risk-critical",
  HIGH: "--color-risk-high",
  MODERATE: "--color-risk-moderate",
  LOW: "--color-risk-low",
};

function formatTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", hour12: false }) + " IST";
}

export default function AlertsPanel({ alerts }) {
  return (
    <section className="panel" aria-labelledby="alerts-heading">
      <div className="panel-header">
        <h2 id="alerts-heading">Alerts &amp; Warnings</h2>
        <span className="eyebrow">{alerts.length} Active</span>
      </div>
      <div className="panel-body alerts-panel__body">
        {alerts.length === 0 && (
          <p className="alerts-panel__empty">No active alerts for the selected location.</p>
        )}
        {alerts.map((alert) => {
          const colorVar = SEVERITY_COLOR_VAR[alert.severity] || "--color-info";
          return (
            <div className="alert-item" key={alert.id} style={{ borderLeftColor: `var(${colorVar})` }}>
              <div className="alert-item__top">
                <span className="alert-item__title" style={{ color: `var(${colorVar})` }}>
                  {alert.title}
                </span>
                <span className="mono alert-item__time">{formatTime(alert.time)}</span>
              </div>
              <p className="alert-item__message">{alert.message}</p>
              <div className="alert-item__meta">
                <span>Location: {alert.zone}</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
