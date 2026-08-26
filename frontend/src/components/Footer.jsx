import "./Footer.css";

export default function Footer({ systemInfo }) {
  return (
    <footer className="app-footer">
      <div className="app-footer__row">
        <span>
          {systemInfo?.systemName || "Urban Flood Nowcasting System"} — Smart India Hackathon Problem Statement{" "}
          {systemInfo?.problemStatementId || "SIH26085"}
        </span>
        <span>{systemInfo?.ministry || "Ministry of Earth Sciences, Government of India"}</span>
      </div>
      <div className="app-footer__row app-footer__row--muted">
        <span>{systemInfo?.dataStatus || "Prototype Data (Mock)"} · Interface for internal-round demonstration purposes.</span>
        <span>Backend and GIS integration pending.</span>
      </div>
    </footer>
  );
}
