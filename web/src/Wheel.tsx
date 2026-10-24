import { useMemo, useState } from "react";
import type { Chart, Point } from "./types";
import {
  SIGNS,
  GLYPHS,
  COLORS,
  polar,
  ringArc,
  formatPosition,
} from "./geometry";
import {
  BANDS as B,
  compactLabels,
  decanDisplayRuler,
  RULER_GLYPHS,
  matchesPoint,
  wheelRotation,
  type Density,
  type Orientation,
} from "./wheelLayout";

export function Wheel({
  chart,
  dual,
  selected,
  onSelect,
  precision,
  orientation,
  density,
  query,
  zoom,
}: {
  chart: Chart;
  dual: boolean;
  selected: string | null;
  onSelect: (id: string) => void;
  precision: "degree" | "minute" | "second";
  orientation: Orientation;
  density: Density;
  query: string;
  zoom: number;
}) {
  const [hovered, setHovered] = useState<string | null>(null);
  const points = useMemo(
    () =>
      chart.points.filter(
        (p): p is Point & { longitude_deg: number } =>
          p.available && p.longitude_deg !== null,
      ),
    [chart],
  );
  const rotation = wheelRotation(chart.angles.Ascendant, orientation);
  const houseStart = Math.floor((chart.angles.Ascendant ?? 0) / 30) * 30;
  const layout = useMemo(
    () => compactLabels(points, rotation, density, zoom, selected, query),
    [points, rotation, density, zoom, selected, query],
  );
  const byId = useMemo(() => new Map(points.map((p) => [p.id, p])), [points]);
  const inspected = byId.get(hovered ?? selected ?? "");
  const fine = zoom >= 2,
    textScale = 1 / Math.sqrt(zoom);
  const labelIds = new Set(layout.labels.map((l) => l.id));
  return (
    <svg
      id="chart-wheel"
      className="compact-wheel"
      viewBox="0 0 1000 1000"
      role="group"
      aria-labelledby="wheel-title wheel-desc"
      xmlns="http://www.w3.org/2000/svg"
      data-orientation={orientation}
      data-rotation={rotation}
      data-marker-count={points.length}
      data-label-count={layout.labels.length}
      data-scale-minutes={fine ? 10 : 60}
    >
      <title id="wheel-title">{chart.input.name} astrology chart</title>
      <desc id="wheel-desc">
        {points.length} calculated objects, all marked at unrounded astronomical
        longitudes. {layout.labels.length} prioritized labels. Search, hover,
        select or use the complete position table to inspect every object.
        Alignment changes the view only.
      </desc>
      <circle
        cx="500"
        cy="500"
        r="488"
        fill="#fff"
        stroke="#d9cfe0"
        strokeWidth=".7"
      />
      <g
        data-band="degree-minute-scale"
        aria-label={
          fine
            ? "Degree scale with ten-minute subdivisions"
            : "Degree scale; zoom to 200 percent for ten-minute subdivisions"
        }
      >
        {Array.from({ length: fine ? 2160 : 360 }, (_, i) => {
          const degree = fine ? i / 6 : i,
            whole = !fine || i % 6 === 0;
          const start = polar(degree, B.scale, rotation),
            end = polar(
              degree,
              whole
                ? Math.round(degree) % 10 === 0
                  ? 486
                  : Math.round(degree) % 5 === 0
                    ? 483
                    : 479
                : 476,
              rotation,
            );
          return (
            <line
              key={i}
              x1={start[0]}
              y1={start[1]}
              x2={end[0]}
              y2={end[1]}
              stroke={whole ? "#786583" : "#b7a9c0"}
              strokeWidth={whole ? 0.7 : 0.35}
            />
          );
        })}
        {Array.from({ length: 36 }, (_, i) => {
          const p = polar(i * 10, 494, rotation);
          return (
            <text
              key={i}
              x={p[0]}
              y={p[1]}
              className="scale-number"
              textAnchor="middle"
              dominantBaseline="middle"
            >
              {(i % 3) * 10}°
            </text>
          );
        })}
      </g>
      <g
        data-band="astronomical-zodiac"
        aria-label="Tropical astronomical zodiac"
      >
        {SIGNS.map((sign, i) => {
          const p = polar(i * 30 + 15, 450, rotation);
          return (
            <g key={sign}>
              <path
                d={ringArc(
                  i * 30,
                  (i + 1) * 30,
                  B.zodiacOuter,
                  B.zodiacInner,
                  rotation,
                )}
                fill={COLORS[i]}
                fillOpacity=".065"
                stroke="#bfb3c7"
                strokeWidth=".7"
              />
              <text
                x={p[0]}
                y={p[1]}
                className="compact-zodiac"
                fill={COLORS[i]}
                textAnchor="middle"
                dominantBaseline="middle"
              >
                {GLYPHS[i]}
                {"\uFE0E"}
              </text>
            </g>
          );
        })}
      </g>
      <g
        data-band="modern-triplicity-decans"
        aria-label="Modern triplicity decan rulers"
      >
        {Array.from({ length: 36 }, (_, i) => {
          const sign = Math.floor(i / 3),
            decan = i % 3,
            ruler = decanDisplayRuler(sign, decan),
            p = polar(i * 10 + 5, 421, rotation);
          return (
            <g
              key={i}
              data-decan-sign={sign}
              data-decan-index={decan}
              data-decan-ruler={ruler}
            >
              <title>
                {SIGNS[sign]} {decan * 10}°–{(decan + 1) * 10}° · {ruler}
              </title>
              <path
                d={ringArc(
                  i * 10,
                  (i + 1) * 10,
                  B.zodiacInner,
                  B.decanInner,
                  rotation,
                )}
                fill="#fbf8fc"
                stroke="#d6cbdc"
                strokeWidth=".55"
              />
              <text
                x={p[0]}
                y={p[1]}
                textAnchor="middle"
                dominantBaseline="middle"
                className="decan-glyph"
              >
                {RULER_GLYPHS[ruler]}
              </text>
            </g>
          );
        })}
      </g>
      <circle
        cx="500"
        cy="500"
        r={B.marker}
        fill="none"
        stroke="#b7a9c1"
        strokeWidth=".6"
      />
      {chart.whole_sign_cusps.length > 0 && (
        <g
          data-band="true-placement-energies"
          aria-label="House-derived True Placement energies"
        >
          {SIGNS.map((sign, i) => {
            const lon = houseStart + i * 30,
              a = polar(lon, B.marker, rotation),
              b = polar(lon, B.energyOuter, rotation),
              p = polar(lon + 15, 203, rotation);
            return (
              <g
                key={sign}
                data-energy-house={i + 1}
                data-energy-sign={sign}
                data-house-cusp={lon % 360}
              >
                <line
                  x1={a[0]}
                  y1={a[1]}
                  x2={b[0]}
                  y2={b[1]}
                  stroke="#dfd5e5"
                  strokeWidth=".65"
                />
                <path
                  d={ringArc(
                    lon,
                    lon + 30,
                    B.energyOuter,
                    B.energyInner,
                    rotation,
                  )}
                  fill={dual ? "#f5ecfa" : "#faf7fc"}
                  stroke="#cbb8d6"
                  strokeWidth=".65"
                />
                {dual ? (
                  <>
                    <text
                      x={p[0]}
                      y={p[1] - 3}
                      textAnchor="middle"
                      dominantBaseline="middle"
                      className="energy-glyph"
                    >
                      {GLYPHS[i]}
                      {"\uFE0E"}
                    </text>
                    <text
                      x={p[0]}
                      y={p[1] + 14}
                      textAnchor="middle"
                      className="energy-caption"
                    >
                      {i + 1} · {sign}
                    </text>
                  </>
                ) : (
                  <text
                    x={p[0]}
                    y={p[1]}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="compact-house"
                  >
                    {i + 1}
                  </text>
                )}
              </g>
            );
          })}
        </g>
      )}
      <g data-band="precise-object-positions">
        {points.map((p) => {
          const a = polar(p.longitude_deg, B.marker, rotation),
            b = polar(p.longitude_deg, 407, rotation),
            active = selected === p.id,
            match = !!query.trim() && matchesPoint(p, query);
          return (
            <g
              key={p.id}
              data-object-id={p.id}
              data-longitude={p.longitude_deg}
              data-labelled={labelIds.has(p.id)}
              role="button"
              tabIndex={0}
              aria-label={`${p.name}, ${formatPosition(p.longitude_deg, precision)}${p.house ? `, House ${p.house}` : ""}`}
              aria-pressed={active}
              className={`exact-object-marker${active ? " selected" : ""}${match ? " search-match" : ""}`}
              onMouseEnter={() => setHovered(p.id)}
              onMouseLeave={() => setHovered(null)}
              onFocus={() => setHovered(p.id)}
              onBlur={() => setHovered(null)}
              onClick={() => onSelect(p.id)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onSelect(p.id);
                }
              }}
            >
              <title>
                {p.name}: {formatPosition(p.longitude_deg, precision)} ·{" "}
                {p.longitude_deg}°{p.retrograde ? " · retrograde" : ""}
              </title>
              <line
                x1={a[0]}
                y1={a[1]}
                x2={b[0]}
                y2={b[1]}
                stroke={active || match ? "#9c00c9" : "#4d3858"}
                strokeWidth={active || match ? 1.8 : 0.7}
              />
              <circle
                data-astronomical-marker="true"
                cx={a[0]}
                cy={a[1]}
                r={active || match ? 3 : 1.7}
                fill={active || match ? "#a100d0" : "#493053"}
              />
              <circle
                cx={a[0]}
                cy={a[1]}
                r="6"
                fill="transparent"
                className="marker-hit"
              />
            </g>
          );
        })}
      </g>
      <g data-band="object-annotations" style={{ fontSize: 20 * textScale }}>
        {layout.labels.map((label) => {
          const p = byId.get(label.id)!,
            a = polar(p.longitude_deg, B.marker, rotation),
            active = p.id === selected;
          return (
            <g
              key={p.id}
              data-label-id={p.id}
              className={`compact-object-label${active ? " selected" : ""}`}
              onMouseEnter={() => setHovered(p.id)}
              onMouseLeave={() => setHovered(null)}
              onClick={() => onSelect(p.id)}
            >
              <title>
                {p.name} · {formatPosition(p.longitude_deg, precision)}
              </title>
              <line
                x1={a[0]}
                y1={a[1]}
                x2={label.x}
                y2={label.y}
                stroke={active ? "#a100d0" : "#c3b4cc"}
                strokeWidth={active ? 1.2 : 0.5}
              />
              <text
                x={label.x}
                y={label.y + 2 * textScale}
                textAnchor="middle"
                className="compact-glyph"
                style={{
                  fontSize: (/^\d+$/.test(p.glyph) ? 13 : 20) * textScale,
                }}
              >
                {p.glyph}
                <tspan className="compact-retro">
                  {p.retrograde ? "℞" : ""}
                </tspan>
              </text>
              <text
                x={label.x}
                y={label.y + 16 * textScale}
                textAnchor="middle"
                className="compact-position"
                style={{ fontSize: 10 * textScale }}
              >
                {formatPosition(p.longitude_deg, precision).split(" ")[0]}
              </text>
            </g>
          );
        })}
      </g>
      <g data-band="angle-indicators">
        {Object.entries({
          Ascendant: "AC",
          Midheaven: "MC",
          Descendant: "DC",
          ImumCoeli: "IC",
        }).map(([id, name]) => {
          const lon = chart.angles[id];
          if (lon === undefined) return null;
          const a = polar(lon, 402, rotation),
            b = polar(lon, 470, rotation),
            c = polar(lon, 459, rotation);
          return (
            <g key={id}>
              <line
                x1={a[0]}
                y1={a[1]}
                x2={b[0]}
                y2={b[1]}
                stroke={id === "Ascendant" ? "#9800c5" : "#846a92"}
                strokeWidth={id === "Ascendant" ? 1.4 : 0.8}
                strokeDasharray={id === "Ascendant" ? undefined : "2 3"}
              />
              <text
                x={c[0]}
                y={c[1]}
                textAnchor="middle"
                dominantBaseline="middle"
                className="compact-angle"
              >
                {name}
              </text>
            </g>
          );
        })}
      </g>
      <g data-band="central-inspection" pointerEvents="none">
        <circle
          cx="500"
          cy="500"
          r={B.center}
          fill="#fff"
          stroke="#e2d6e9"
          strokeWidth=".7"
        />
        <text x="500" y="406" textAnchor="middle" className="center-brand">
          Mystic Rebels
        </text>
        {inspected ? (
          <>
            <text
              x="500"
              y="438"
              textAnchor="middle"
              className="center-context"
            >
              {hovered && hovered !== selected
                ? "Hover preview"
                : "Selected object"}
            </text>
            <text x="500" y="480" textAnchor="middle" className="center-glyph">
              {inspected.glyph}
            </text>
            <text
              x="500"
              y="508"
              textAnchor="middle"
              className="center-object"
              style={{ fontSize: inspected.name.length > 25 ? 11 : 14 }}
            >
              {inspected.name}
            </text>
            <text
              x="500"
              y="534"
              textAnchor="middle"
              className="center-position"
            >
              {formatPosition(inspected.longitude_deg, precision)}
            </text>
            <text
              x="500"
              y="560"
              textAnchor="middle"
              className="center-details"
            >
              {inspected.house
                ? `House ${inspected.house} · ${inspected.field}`
                : "House unavailable"}
            </text>
            <text
              x="500"
              y="580"
              textAnchor="middle"
              className="center-details"
            >
              Tone {inspected.tone} · Pulse {inspected.pulse}
            </text>
          </>
        ) : (
          <text x="500" y="505" textAnchor="middle" className="center-details">
            Select an object to inspect
          </text>
        )}
        <text x="500" y="612" textAnchor="middle" className="center-context">
          {points.length} markers · {layout.labels.length} labels
        </text>
        <text x="500" y="630" textAnchor="middle" className="center-context">
          {chart.time.time_is_reference_only ? "Time uncertain" : "Whole Sign"}
        </text>
      </g>
    </svg>
  );
}
