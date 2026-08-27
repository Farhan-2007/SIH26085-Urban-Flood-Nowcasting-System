import GISMap from "./gis/GISMap";
import "./FloodMap.css";

export default function FloodMap({ zones }) {
  return (
    <section className="panel flood-map">
      <div className="panel-header">
        <h2>Geographic Flood-Risk Map</h2>
        <span className="eyebrow">GIS Map</span>
      </div>

      <div className="panel-body">
        <GISMap zones={zones} />
      </div>
    </section>
  );
}