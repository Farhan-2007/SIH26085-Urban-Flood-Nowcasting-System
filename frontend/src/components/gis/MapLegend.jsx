const risks = [
  ["LOW", "#22c55e"],
  ["MEDIUM", "#eab308"],
  ["HIGH", "#f97316"],
  ["CRITICAL", "#ef4444"],
];

export default function MapLegend() {
  return (
    <div
      style={{
        position: "absolute",
        bottom: 20,
        left: 20,
        background: "white",
        padding: 12,
        borderRadius: 8,
        zIndex: 1000,
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
            marginTop: 6,
          }}
        >
          <span
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              background: color,
            }}
          />

          <span>{label}</span>
        </div>
      ))}
    </div>
  );
}