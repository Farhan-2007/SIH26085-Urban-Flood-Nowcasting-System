import "./AlertsPanel.css";

const SEVERITY_COLOR_VAR = {
  CRITICAL: "--color-risk-critical",
  HIGH: "--color-risk-high",
  MODERATE: "--color-risk-moderate",
  LOW: "--color-risk-low",
};

export default function AlertsPanel({ alerts }) {
  return (
    <section className="panel" aria-labelledby="alerts-heading">
      <div className="panel-header">
        <h2 id="alerts-heading">Alerts &amp; Warnings</h2>
        <span className="eyebrow">{alerts.length} Active · Prototype Data</span>
      </div>
      <div className="panel-body alerts-panel__body">
        {alerts.length === 0 && <p className="alerts-panel__empty">No active alerts for the monitored zone.</p>}
        {alerts.map((alert) => {
          const colorVar = SEVERITY_COLOR_VAR[alert.severity] || "--color-info";
          return (
            <div className="alert-item" key={alert.id} style={{ borderLeftColor: `var(${colorVar})` }}>
              <div className="alert-item__top">
                <span className="alert-item__title" style={{ color: `var(${colorVar})` }}>
                  {alert.title}
                </span>
                <span className="mono alert-item__time">{alert.time}</span>
              </div>
              <p className="alert-item__message">{alert.message}</p>
              <div className="alert-item__meta">
                <span>Zone: {alert.zone}</span>
                <span className="mono">{alert.id}</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
