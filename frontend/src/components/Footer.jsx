import "./Footer.css";

export default function Footer() {
  return (
    <footer className="app-footer">
      <div className="app-footer__row">
        <span>Urban Flood Nowcasting System</span>
        <span>Ministry of Earth Sciences, Government of India</span>
      </div>
      <div className="app-footer__row app-footer__row--muted">
        <span>Drainage and Rainfall Coupling — Street-Level Flood Risk Nowcasting</span>
        <span>GIS module integration in progress</span>
      </div>
    </footer>
  );
}
