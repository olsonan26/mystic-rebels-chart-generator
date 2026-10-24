import { describe, it, expect } from "vitest";
import { formatPosition, formatDegreeOnly, placeLabels, polar, normalize } from "./geometry";
describe("raw chart geometry", () => {
  it("retains the exact longitude when allocating crowded labels", () => {
    const points = Array.from({ length: 45 }, (_, i) => ({
      id: `p${i}`,
      longitude_deg: 120 + i * 0.0001,
    }));
    const labels = placeLabels(points);
    expect(labels).toHaveLength(points.length);
    for (const p of points)
      expect(labels.find((l) => l.id === p.id)?.actual).toBe(p.longitude_deg);
    for (const l of labels) {
      expect(Number.isFinite(l.angle)).toBe(true);
      expect(l.radius).toBeGreaterThan(100);
    }
  });
  it("keeps 72 dense labels separate at the actual chart rotation", () => {
    const rotation = 296.5674;
    const points = Array.from({ length: 72 }, (_, i) => ({
      id: `p${i}`,
      longitude_deg: 120 + i * 0.0001,
    }));
    const labels = placeLabels(points, rotation);
    for (let i = 0; i < labels.length; i++)
      for (let j = i + 1; j < labels.length; j++) {
        const a = polar(labels[i].angle, labels[i].radius, rotation),
          b = polar(labels[j].angle, labels[j].radius, rotation);
        expect(Math.abs(a[0] - b[0]) >= 78 || Math.abs(a[1] - b[1]) >= 40).toBe(
          true,
        );
      }
  });
  it("uses identical unrounded longitude for actual SVG geometry", () => {
    const raw = 115.74014204831833;
    const [x, y] = polar(raw, 373, 296.5674361399037);
    const inverse = normalize(
      (Math.atan2(500 - y, x - 500) * 180) / Math.PI - 180 + 296.5674361399037,
    );
    expect(Math.abs(inverse - raw)).toBeLessThan(1e-12);
  });
  it("places AC left and the independent MC above the horizon", () => {
    const ac = 296.5674361399037,
      mc = 225.82482012873805;
    expect(polar(ac, 373, ac)[0]).toBeCloseTo(127, 10);
    expect(polar(mc, 373, ac)[1]).toBeLessThan(500);
    expect(polar(ac + 30, 373, ac)[1]).toBeGreaterThan(500);
  });
  it("carries seconds at the sign boundary without changing raw coordinates", () => {
    const raw = 29.9999999;
    expect(formatPosition(raw)).toBe("0°00′00″ Taurus");
    expect(raw).toBe(29.9999999);
  });
  it("displays only the original numeric position while sign remains separate", () => {
    expect(formatDegreeOnly(115.74027777777778)).toBe("25°44′25″");
    expect(formatDegreeOnly(359.5, "minute")).toBe("29°30′");
    expect(formatDegreeOnly(29.9999999)).toBe("0°00′00″");
    expect(formatPosition(115.74027777777778)).toBe("25°44′25″ Cancer");
  });
  it("formats wrap and minute precision correctly", () => {
    expect(formatPosition(360)).toBe("0°00′00″ Aries");
    expect(formatPosition(-0.5, "minute")).toBe("29°30′ Pisces");
  });
});
