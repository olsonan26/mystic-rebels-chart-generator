import { normalize, polar } from "./geometry";
export type Orientation = "ascendant" | "whole-sign";
export type Density = "sparse" | "balanced" | "detailed" | "all";
export type LayoutPoint = {
  id: string;
  name: string;
  group: string;
  longitude_deg: number;
};
export const BANDS = {
  scale: 474,
  zodiacOuter: 468,
  zodiacInner: 432,
  decanInner: 410,
  marker: 400,
  energyOuter: 224,
  energyInner: 183,
  center: 168,
} as const;
// Display legend only: exactly the modern ruler order already used by placements.py.
export const MODERN_RULERS = [
  "Mars",
  "Venus",
  "Mercury",
  "Moon",
  "Sun",
  "Mercury",
  "Venus",
  "Pluto",
  "Jupiter",
  "Saturn",
  "Uranus",
  "Neptune",
];
export const RULER_GLYPHS: Record<string, string> = {
  Mars: "♂",
  Venus: "♀",
  Mercury: "☿",
  Moon: "☽",
  Sun: "☉",
  Pluto: "♇",
  Jupiter: "♃",
  Saturn: "♄",
  Uranus: "♅",
  Neptune: "♆",
};
export const decanDisplayRuler = (sign: number, decan: number) =>
  MODERN_RULERS[(sign + 4 * decan) % 12];
export function wheelRotation(
  ascendant: number | undefined,
  orientation: Orientation,
) {
  const ac = ascendant ?? 0;
  return orientation === "whole-sign" ? Math.floor(ac / 30) * 30 : ac;
}
export function matchesPoint(p: LayoutPoint, query: string) {
  return `${p.name} ${p.id}`.toLowerCase().includes(query.trim().toLowerCase());
}
export type CompactLabel = {
  id: string;
  actual: number;
  angle: number;
  radius: number;
  x: number;
  y: number;
};
export function compactLabels(
  points: LayoutPoint[],
  rotation: number,
  density: Density,
  zoom: number,
  selected: string | null,
  query: string,
) {
  const scale = Math.sqrt(zoom),
    width = 62 / scale,
    height = 44 / scale;
  const target =
    density === "all"
      ? points.length
      : Math.round({ sparse: 18, balanced: 48, detailed: 88 }[density] * zoom);
  // Prioritize source-significant objects before lower-priority research bodies.
  // Sorting within each priority remains by true unrounded longitude.
  const ranks: Record<string, number> = {
    Angles: 460,
    Planets: 450,
    "Lunar points": 435,
    Asteroids: 200,
    Parts: 150,
    "Minor bodies": 100,
  };
  const maxLabelDriftDegrees = 24; // display-only: never relocate astronomical anchors
  const score = (p: LayoutPoint) =>
    (p.id === selected ? 10000 : 0) +
    (query.trim() && matchesPoint(p, query) ? 5000 : 0) +
    (ranks[p.group] ?? 0);
  const ordered = [...points].sort(
    (a, b) =>
      score(b) - score(a) ||
      a.longitude_deg - b.longitude_deg ||
      (a.id < b.id ? -1 : a.id > b.id ? 1 : 0),
  );
  const occupied = new Map<string, [number, number][]>();
  const key = (x: number, y: number) =>
    `${Math.floor(x / width)},${Math.floor(y / height)}`;
  const fits = (x: number, y: number) => {
    for (const dx of [-width / 2, width / 2])
      for (const dy of [-height / 2, height / 2]) {
        const radius = Math.hypot(x + dx - 500, y + dy - 500);
        if (radius < 230 || radius > 396) return false;
      }
    const gx = Math.floor(x / width),
      gy = Math.floor(y / height);
    for (let dx = -1; dx <= 1; dx++)
      for (let dy = -1; dy <= 1; dy++)
        for (const [px, py] of occupied.get(`${gx + dx},${gy + dy}`) ?? [])
          if (Math.abs(x - px) < width && Math.abs(y - py) < height)
            return false;
    return true;
  };
  const labels: CompactLabel[] = [];
  const laneStep = height / 2 + 1,
    lanes = Math.max(1, Math.floor((376 - 240) / laneStep) + 1);
  for (const p of ordered) {
    if (labels.length >= target) break;
    let found: CompactLabel | undefined;
    // Spatial hashing keeps hundreds bounded; only annotation positions move.
    for (let shift = 0; shift <= maxLabelDriftDegrees && !found; shift += 2) {
      for (const direction of shift === 0 ? [1] : [1, -1]) {
        for (let lane = 0; lane < lanes; lane++) {
          const radius = 376 - lane * laneStep,
            angle = normalize(p.longitude_deg + direction * shift);
          // Preserve the astronomical sign sector even for the annotation.
          if (Math.floor(angle / 30) !== Math.floor(normalize(p.longitude_deg) / 30))
            continue;
          const [x, y] = polar(angle, radius, rotation);
          if (fits(x, y)) {
            found = { id: p.id, actual: p.longitude_deg, angle, radius, x, y };
            break;
          }
        }
        if (found) break;
      }
    }
    if (found) {
      const cell = key(found.x, found.y),
        list = occupied.get(cell) ?? [];
      list.push([found.x, found.y]);
      occupied.set(cell, list);
      labels.push(found);
    }
    // A full annotation band never removes or throws away an astronomical point.
  }
  return { labels, requested: Math.min(target, points.length), width, height, maxLabelDriftDegrees };
}
