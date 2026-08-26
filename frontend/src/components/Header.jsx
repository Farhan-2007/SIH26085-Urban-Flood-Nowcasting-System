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

export default function Header({ systemInfo }) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="app-header">
      <div className="app-header__top">
        <span>{systemInfo?.ministry || "Ministry of Earth Sciences, Government of India"}</span>
      </div>

      <div className="app-header__main">
        <div className="app-header__identity">
          <div className="app-header__emblem" aria-hidden="true">
            <span>MoES</span>
          </div>
          <div>
            <h1 className="app-header__title">
              {systemInfo?.systemName || "Urban Flood Nowcasting System"}
            </h1>
            <p className="app-header__subtitle">
              {systemInfo?.subtitle || "Drainage and Rainfall Coupling"} · Problem Statement{" "}
              {systemInfo?.problemStatementId || "SIH26085"}
            </p>
          </div>
        </div>

        <div className="app-header__status">
          <div className="app-header__status-item">
            <span className="app-header__status-dot" aria-hidden="true" />
            <span>System Online</span>
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
