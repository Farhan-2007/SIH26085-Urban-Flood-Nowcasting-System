import { RISK_LEVEL_META } from "../utils/riskLevel";
import { useAnimatedNumber } from "../hooks/useAnimatedNumber";
import "./RiskGauge.css";

// A semi-circular instrument gauge, styled after analogue monitoring
// dials rather than a decorative "progress ring". Tick marks and the
// four risk bands are always visible so the needle position reads
// against a fixed scale, the way a physical gauge would. The needle
// rotates smoothly between values instead of snapping, so switching
// forecast steps reads as a live instrument responding to new data.
const SIZE = 220;
const CENTER = SIZE / 2;
const RADIUS = 92;
const NEEDLE_LENGTH = RADIUS - 14;
const START_ANGLE = -180; // degrees, left end of the arc (score = 0)
const END_ANGLE = 0; // degrees, right end of the arc (score = 100)

function angleForScore(score) {
  const clamped = Math.max(0, Math.min(100, score));
  return START_ANGLE + (clamped / 100) * (END_ANGLE - START_ANGLE);
}

function polarToCartesian(cx, cy, r, angleDeg) {
  const angleRad = (angleDeg * Math.PI) / 180;
  return {
    x: cx + r * Math.cos(angleRad),
    y: cy + r * Math.sin(angleRad),
  };
}

function describeArc(cx, cy, r, startAngle, endAngle) {
  const start = polarToCartesian(cx, cy, r, startAngle);
  const end = polarToCartesian(cx, cy, r, endAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1;
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArcFlag} 1 ${end.x} ${end.y}`;
}

const BANDS = [
  { level: "LOW", from: 0, to: 25 },
  { level: "MODERATE", from: 25, to: 50 },
  { level: "HIGH", from: 50, to: 75 },
  { level: "CRITICAL", from: 75, to: 100 },
];

export default function RiskGauge({ score, level }) {
  const meta = RISK_LEVEL_META[level];
  const animatedScore = useAnimatedNumber(score);
  // Needle rotates from a fixed "pointing left" pose (0deg rotation, score 0)
  // through to "pointing right" (180deg rotation, score 100).
  const needleRotation = angleForScore(animatedScore) - START_ANGLE;
  const ticks = Array.from({ length: 11 }, (_, i) => i * 10);

  return (
    <div className={`risk-gauge risk-gauge--${level.toLowerCase()}`}>
      <svg
        viewBox={`0 0 ${SIZE} ${SIZE * 0.62}`}
        className="risk-gauge__svg"
        role="img"
        aria-label={`Flood risk score ${score} out of 100, level ${level}`}
      >
        {BANDS.map((band) => (
          <path
            key={band.level}
            d={describeArc(CENTER, CENTER, RADIUS, angleForScore(band.from), angleForScore(band.to))}
            stroke={`var(${RISK_LEVEL_META[band.level].colorVar})`}
            strokeWidth={10}
            fill="none"
            strokeLinecap="butt"
            opacity={0.85}
          />
        ))}

        {ticks.map((t) => {
          const a = angleForScore(t);
          const outer = polarToCartesian(CENTER, CENTER, RADIUS + 8, a);
          const inner = polarToCartesian(CENTER, CENTER, RADIUS + (t % 20 === 0 ? 1 : 3), a);
          return (
            <line
              key={t}
              x1={inner.x}
              y1={inner.y}
              x2={outer.x}
              y2={outer.y}
              stroke="var(--color-border-strong)"
              strokeWidth={t % 20 === 0 ? 1.5 : 1}
            />
          );
        })}

        <g
          className="risk-gauge__needle-group"
          style={{
            transform: `rotate(${needleRotation}deg)`,
            transformOrigin: `${CENTER}px ${CENTER}px`,
          }}
        >
          <line
            x1={CENTER}
            y1={CENTER}
            x2={CENTER - NEEDLE_LENGTH}
            y2={CENTER}
            stroke="var(--color-navy-900)"
            strokeWidth={2.5}
            strokeLinecap="round"
          />
        </g>
        <circle cx={CENTER} cy={CENTER} r={5} fill="var(--color-navy-900)" />
      </svg>

      <div className="risk-gauge__readout">
        <span className="risk-gauge__score mono" style={{ color: `var(${meta.colorVar})` }}>
          {Math.round(animatedScore)}
        </span>
        <span className="risk-gauge__scale">/ 100</span>
      </div>
    </div>
  );
}
