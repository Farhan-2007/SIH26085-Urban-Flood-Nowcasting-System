import GISMap from "./gis/GISMap";
import "./FloodMap.css";

export default function FloodMap({
  zones,
  selected,
  analysis,
}) {
  return (
    <section className="panel flood-map">
      <div className="panel-header">
        <h2>Geographic Flood-Risk Map</h2>

        <span className="eyebrow">
          {selected?.label === "NOW"
            ? "Real-time GIS Assessment"
            : `Forecast: ${selected?.label || "GIS Map"}`}
        </span>
      </div>

      <div className="panel-body">
        <GISMap
          zones={zones}
          selected={selected}
          analysis={analysis}
        />
      </div>
    </section>
  );
}