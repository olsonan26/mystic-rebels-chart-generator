import { useMemo } from "react";
import type { Chart, Point } from "./types";
import {
  SIGNS,
  GLYPHS,
  COLORS,
  polar,
  ringArc,
  placeLabels,
  formatPosition,
} from "./geometry";
export function LegacyWheel({
  chart,
  dual,
  selected,
  onSelect,
  precision,
}: {
  chart: Chart;
  dual: boolean;
  selected: string | null;
  onSelect: (id: string) => void;
  precision: "degree" | "minute" | "second";
}) {
  const points = chart.points.filter(
    (p): p is Point & { longitude_deg: number } =>
      p.available && p.longitude_deg !== null,
  );
  const rotation = chart.angles.Ascendant ?? 0;
  const houseStart = Math.floor(rotation / 30) * 30;
  const labels = useMemo(() => placeLabels(points, rotation), [chart]);
  return (
    <svg
      id="chart-wheel"
      viewBox="0 0 1000 1000"
      role="img"
      aria-labelledby="wheel-title wheel-desc"
      xmlns="http://www.w3.org/2000/svg"
    >
      <title id="wheel-title">{chart.input.name} astrology chart</title>
      <desc id="wheel-desc">
        {points.length} calculated objects at their exact astronomical
        longitudes. Select an object to inspect its position. Text positions are
        also available in the accompanying table.
      </desc>
      <circle cx="500" cy="500" r="473" fill="#fff" stroke="#e8dfed" />
      {SIGNS.map((sign, i) => (
        <g key={sign}>
          <path
            d={ringArc(i * 30, (i + 1) * 30, 438, 378, rotation)}
            fill={COLORS[i]}
            fillOpacity=".07"
            stroke="#dcd2e1"
            strokeWidth=".8"
          />
          <text
            x={polar(i * 30 + 15, 408, rotation)[0]}
            y={polar(i * 30 + 15, 408, rotation)[1]}
            textAnchor="middle"
            dominantBaseline="middle"
            className="zodiac"
            fill={COLORS[i]}
          >
            {GLYPHS[i]}
          </text>
        </g>
      ))}
      {Array.from({ length: 360 }, (_, i) => {
        const a = polar(i, 438, rotation),
          b = polar(i, i % 10 === 0 ? 450 : i % 5 === 0 ? 446 : 442, rotation);
        return (
          <line
            key={i}
            x1={a[0]}
            y1={a[1]}
            x2={b[0]}
            y2={b[1]}
            stroke="#876d91"
            strokeWidth={i % 30 === 0 ? 1.5 : 0.65}
          />
        );
      })}
      {chart.whole_sign_cusps.length > 0 &&
        SIGNS.map((sign, i) => {
          const lon = houseStart + i * 30,
            a = polar(lon, 377, rotation),
            b = polar(lon, 108, rotation),
            p = polar(lon + 15, dual ? 348 : 133, rotation);
          return (
            <g key={sign}>
              <line
                x1={a[0]}
                y1={a[1]}
                x2={b[0]}
                y2={b[1]}
                stroke="#cbbbd1"
                strokeWidth=".9"
              />
              {dual ? (
                <>
                  <path
                    d={ringArc(lon, lon + 30, 376, 324, rotation)}
                    fill="#f8f1fb"
                    stroke="#e3d7e8"
                  />
                  <text
                    x={p[0]}
                    y={p[1] - 4}
                    className="house-energy"
                    textAnchor="middle"
                  >
                    {GLYPHS[i]} {SIGNS[i]}
                  </text>
                  <text
                    x={p[0]}
                    y={p[1] + 13}
                    className="house-small"
                    textAnchor="middle"
                  >
                    House {i + 1}
                  </text>
                </>
              ) : (
                <text
                  x={p[0]}
                  y={p[1]}
                  className="house"
                  textAnchor="middle"
                  dominantBaseline="middle"
                >
                  {i + 1}
                </text>
              )}
            </g>
          );
        })}
      <circle cx="500" cy="500" r="108" fill="#fff" stroke="#e6dbec" />
      <text x="500" y="491" className="wheel-center" textAnchor="middle">
        Mystic
      </text>
      <text x="500" y="518" className="wheel-center" textAnchor="middle">
        Rebels
      </text>
      <text x="500" y="543" className="house-small" textAnchor="middle">
        {chart.time.time_is_reference_only ? "Time uncertain" : "Whole Sign"}
      </text>
      {["Ascendant", "Midheaven", "Descendant", "ImumCoeli"].map((id) => {
        const lon = chart.angles[id];
        if (lon === undefined) return null;
        const a = polar(lon, 378, rotation),
          b = polar(lon, 461, rotation),
          c = polar(lon, 469, rotation);
        return (
          <g key={id}>
            <line
              x1={a[0]}
              y1={a[1]}
              x2={b[0]}
              y2={b[1]}
              stroke={id === "Ascendant" ? "#a100d0" : "#7c6288"}
              strokeWidth={id === "Ascendant" ? 2 : 1}
              strokeDasharray={id === "Ascendant" ? undefined : "3 3"}
            />
            <text
              x={c[0]}
              y={c[1]}
              className="angle-label"
              textAnchor="middle"
              dominantBaseline="middle"
            >
              {
                {
                  Ascendant: "AC",
                  Midheaven: "MC",
                  Descendant: "DC",
                  ImumCoeli: "IC",
                }[id]
              }
            </text>
          </g>
        );
      })}
      {points.map((p) => {
        const label = labels.find((l) => l.id === p.id)!;
        const pos = polar(p.longitude_deg, dual ? 321 : 373, rotation),
          lp = polar(label.angle, label.radius, rotation);
        const active = selected === p.id;
        return (
          <g
            key={p.id}
            data-object-id={p.id}
            data-longitude={p.longitude_deg}
            tabIndex={0}
            role="button"
            aria-label={`${p.name}, ${formatPosition(p.longitude_deg, precision)}${p.house ? `, House ${p.house}` : ""}`}
            aria-pressed={active}
            onClick={() => onSelect(p.id)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelect(p.id);
              }
            }}
            className={"wheel-object" + (active ? " active" : "")}
          >
            <title>
              {p.name}: {formatPosition(p.longitude_deg, precision)}
              {p.retrograde ? " retrograde" : ""}
            </title>
            <line
              x1={pos[0]}
              y1={pos[1]}
              x2={lp[0]}
              y2={lp[1]}
              stroke={active ? "#a100d0" : "#ac9ab6"}
              strokeWidth={active ? 1.8 : 0.65}
            />
            <circle
              cx={pos[0]}
              cy={pos[1]}
              r={active ? 4 : 2.6}
              fill={active ? "#a100d0" : "#57415f"}
            />
            <rect
              x={lp[0] - 37}
              y={lp[1] - 18}
              width="74"
              height="36"
              rx="8"
              fill={active ? "#f1d7fb" : "#fff"}
              stroke={active ? "#b20ce1" : "none"}
            />
            <text
              x={lp[0]}
              y={lp[1] + 1}
              textAnchor="middle"
              className={
                p.glyph.length > 3 ? "body-glyph numbered" : "body-glyph"
              }
              fill="#4d235c"
            >
              {p.glyph}
              <tspan className="retro" dx="2">
                {p.retrograde ? "℞" : ""}
              </tspan>
            </text>
            <text
              x={lp[0]}
              y={lp[1] + 15}
              textAnchor="middle"
              className="body-degree"
            >
              {formatPosition(p.longitude_deg, precision).split(" ")[0]}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
