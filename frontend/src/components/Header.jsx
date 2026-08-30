import { useEffect, useState } from "react";
import "./Header.css";

function formatTimestamp(date) {
  return date
    .toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    })
    .replace(",", "");
}

const STATUS_META = {
  loading: { label: "Connecting…", className: "app-header__status-dot--loading" },
  ready: { label: "System Online", className: "app-header__status-dot--online" },
  error: { label: "Connection Lost", className: "app-header__status-dot--error" },
};

export default function Header({ apiStatus = "loading" }) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  const status = STATUS_META[apiStatus] || STATUS_META.loading;

  return (
    <header className="app-header">
      <div className="app-header__top">
        <span>Ministry of Earth Sciences, Government of India</span>
      </div>

      <div className="app-header__main">
        <div className="app-header__identity">
          <div className="app-header__emblem" aria-hidden="true">
            <span>MoES</span>
          </div>
          <div>
            <h1 className="app-header__title">Urban Flood Nowcasting System</h1>
            <p className="app-header__subtitle">Drainage and Rainfall Coupling</p>
          </div>
        </div>

        <div className="app-header__status">
          <div className="app-header__status-item">
            <span className={`app-header__status-dot ${status.className}`} aria-hidden="true" />
            <span>{status.label}</span>
          </div>
          <div className="app-header__status-item app-header__status-item--time">
            <span className="eyebrow" style={{ color: "var(--color-text-on-dark-muted)" }}>
              Current Time (IST)
            </span>
            <span className="mono app-header__clock">{formatTimestamp(now)}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
