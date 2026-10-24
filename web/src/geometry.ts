export const SIGNS = [
  "Aries",
  "Taurus",
  "Gemini",
  "Cancer",
  "Leo",
  "Virgo",
  "Libra",
  "Scorpio",
  "Sagittarius",
  "Capricorn",
  "Aquarius",
  "Pisces",
];
export const GLYPHS = [
  "♈",
  "♉",
  "♊",
  "♋",
  "♌",
  "♍",
  "♎",
  "♏",
  "♐",
  "♑",
  "♒",
  "♓",
];
export const COLORS = [
  "#c45239",
  "#62834b",
  "#977039",
  "#457f99",
  "#c45239",
  "#62834b",
  "#977039",
  "#457f99",
  "#c45239",
  "#62834b",
  "#977039",
  "#457f99",
];
export const normalize = (n: number) => ((n % 360) + 360) % 360;
// AC sits on the left; zodiac longitude increases counterclockwise.
export function polar(
  longitude: number,
  radius: number,
  rotation: number,
): [number, number] {
  const a = ((180 + (longitude - rotation)) * Math.PI) / 180;
  return [500 + radius * Math.cos(a), 500 - radius * Math.sin(a)];
}
export function ringArc(
  start: number,
  end: number,
  outer: number,
  inner: number,
  rotation: number,
) {
  const a = polar(start, outer, rotation),
    b = polar(end, outer, rotation),
    c = polar(end, inner, rotation),
    d = polar(start, inner, rotation);
  return `M${a.join(",")}A${outer},${outer} 0 0 0 ${b.join(",")}L${c.join(",")}A${inner},${inner} 0 0 1 ${d.join(",")}Z`;
}
export function formatPosition(
  longitude: number,
  precision: "degree" | "minute" | "second" = "second",
) {
  const factor =
    precision === "degree" ? 1 : precision === "minute" ? 60 : 3600;
  const total = Math.round(normalize(longitude) * factor) % (360 * factor);
  const sign = Math.floor(total / (30 * factor));
  const within = total % (30 * factor);
  const deg = Math.floor(within / factor);
  if (precision === "degree") return `${deg}° ${SIGNS[sign]}`;
  const min = Math.floor((within % factor) / (factor / 60));
  if (precision === "minute")
    return `${deg}°${String(min).padStart(2, "0")}′ ${SIGNS[sign]}`;
  return `${deg}°${String(min).padStart(2, "0")}′${String(within % 60).padStart(2, "0")}″ ${SIGNS[sign]}`;
}
export type LabelPosition = {
  id: string;
  actual: number;
  angle: number;
  radius: number;
};
// Search horizontal label boxes across circular lanes. True markers never move.
export function placeLabels(
  points: { id: string; longitude_deg: number }[],
  rotation = 0,
): LabelPosition[] {
  const occupied: [number, number][] = [];
  return [...points]
    .sort((a, b) => a.longitude_deg - b.longitude_deg)
    .map((p) => {
      let best: {
        angle: number;
        radius: number;
        cost: number;
        xy: [number, number];
      } | null = null;
      for (let shift = 0; shift <= 180; shift++) {
        if (best && shift > best.cost) break;
        for (const direction of shift === 0 ? [1] : [1, -1])
          for (let lane = 0; lane < 5; lane++) {
            const angle = normalize(p.longitude_deg + direction * shift),
              radius = 302 - lane * 39,
              cost = shift + lane * 3;
            if (best && cost >= best.cost) continue;
            const xy = polar(angle, radius, rotation);
            if (
              occupied.every(
                ([x, y]) =>
                  Math.abs(x - xy[0]) >= 78 || Math.abs(y - xy[1]) >= 40,
              )
            )
              best = { angle, radius, cost, xy };
          }
      }
      if (!best)
        for (let shift = 0; shift < 360; shift++) {
          const angle = normalize(p.longitude_deg + shift),
            xy = polar(angle, 465, rotation);
          if (
            occupied.every(
              ([x, y]) =>
                Math.abs(x - xy[0]) >= 78 || Math.abs(y - xy[1]) >= 40,
            )
          ) {
            best = { angle, radius: 465, cost: shift, xy };
            break;
          }
        }
      if (!best)
        throw new Error(
          "Chart label capacity exceeded. Reduce the selected objects.",
        );
      occupied.push(best.xy);
      return {
        id: p.id,
        actual: p.longitude_deg,
        angle: best.angle,
        radius: best.radius,
      };
    });
}

// Present the same rounded degree/minute/second value without a zodiac sign.
// Numeric Position and Astronomical Sign/Tone are separate UI columns; the
// unrounded absolute longitude is never changed.
export function formatDegreeOnly(
  longitude: number,
  precision: "degree" | "minute" | "second" = "second",
) {
  return formatPosition(longitude, precision).split(" ")[0];
}
