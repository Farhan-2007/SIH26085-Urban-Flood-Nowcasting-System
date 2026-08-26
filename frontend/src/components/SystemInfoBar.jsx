import "./SystemInfoBar.css";

function formatUpdated(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

export default function SystemInfoBar({ systemInfo, lastUpdated }) {
  if (!systemInfo) return null;

  const items = [
    { label: "Problem Statement", value: systemInfo.problemStatementId },
    { label: "Scope", value: systemInfo.problemStatement },
    { label: "Forecast Horizon", value: systemInfo.forecastHorizon },
    { label: "Key Inputs", value: systemInfo.keyInputs },
    { label: "Monitored Zone", value: systemInfo.monitoredZone },
  ];

  return (
    <div className="info-bar">
      <div className="info-bar__items">
        {items.map((item) => (
          <div className="info-bar__item" key={item.label}>
            <span className="eyebrow">{item.label}</span>
            <span className="info-bar__value">{item.value}</span>
          </div>
        ))}
      </div>
      <div className="info-bar__meta">
        <span className="info-bar__data-status">{systemInfo.dataStatus}</span>
        <span className="info-bar__updated">
          Last updated <span className="mono">{formatUpdated(lastUpdated)}</span> IST
        </span>
      </div>
    </div>
  );
}
