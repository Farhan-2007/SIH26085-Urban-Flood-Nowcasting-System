const risks = [
  ["Low", "#22c55e"],
  ["Moderate", "#eab308"],
  ["High", "#f97316"],
  ["Critical", "#ef4444"],
];

export default function MapLegend() {
  return (
    <div
      style={{
        position: "absolute",
        bottom: 20,
        left: 20,
        zIndex: 1000,
        background: "white",
        padding: "12px 14px",
        borderRadius: 8,
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
        fontSize: 13,
      }}
    >
      <strong>Flood Risk</strong>

      {risks.map(([label, color]) => (
        <div
          key={label}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginTop: 8,
          }}
        >
          <span
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              background: color,
              display: "inline-block",
            }}
          />

          <span>{label}</span>
        </div>
      ))}
    </div>
  );
}