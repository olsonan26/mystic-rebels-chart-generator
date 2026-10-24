import React from "react";
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { Wheel } from "./Wheel";
import { LegacyWheel } from "./LegacyWheel";
import {
  BANDS,
  compactLabels,
  decanDisplayRuler,
  wheelRotation,
  type LayoutPoint,
} from "./wheelLayout";
import { polar, normalize } from "./geometry";
import type { Chart, Point } from "./types";
import before from "./__fixtures__/wheel-before.json";
const chart = before.chart as unknown as Chart;
const points = chart.points.filter((p) => p.available) as (Point & {
  longitude_deg: number;
})[];
const stress = (count: number): LayoutPoint[] =>
  Array.from({ length: count }, (_, i) => ({
    id: `asteroid-${String(i).padStart(4, "0")}`,
    name: `Object ${i}`,
    group: "Minor bodies",
    longitude_deg: 120 + i * 0.000001,
  }));
describe("presentation-only wheel regression", () => {
  it("matches all 36 recorded modern triplicity decan rulers", () => {
    for (const ref of before.decans)
      expect(decanDisplayRuler(ref.sign_index, ref.decan_index)).toBe(
        ref.ruler,
      );
  });
  it("uses the rising sign boundary at left without changing chart houses", () => {
    const frozen = JSON.stringify(chart),
      ac = chart.angles.Ascendant;
    expect(wheelRotation(ac, "ascendant")).toBe(ac);
    expect(wheelRotation(ac, "whole-sign")).toBe(270);
    expect(polar(270, BANDS.marker, 270)[0]).toBeCloseTo(100, 10);
    for (const orientation of ["ascendant", "whole-sign"] as const) {
      for (const p of points) {
        const rotation = wheelRotation(ac, orientation),
          [x, y] = polar(p.longitude_deg, BANDS.marker, rotation);
        const inverse = normalize(
          (Math.atan2(500 - y, x - 500) * 180) / Math.PI - 180 + rotation,
        );
        expect(
          Math.abs(((inverse - p.longitude_deg + 180) % 360) - 180),
        ).toBeLessThan(1e-10);
      }
    }
    expect(JSON.stringify(chart)).toBe(frozen);
  });
  it("packs hundreds deterministically without collisions or a capacity exception", () => {
    const data = stress(500),
      saved = JSON.stringify(data);
    const a = compactLabels(data, 296.5674, "all", 1, "asteroid-0499", "");
    const b = compactLabels(
      [...data].reverse(),
      296.5674,
      "all",
      1,
      "asteroid-0499",
      "",
    );
    expect(a).toEqual(b);
    expect(a.labels[0].id).toBe("asteroid-0499");
    expect(a.labels.length).toBeGreaterThan(6);
    expect(a.labels.length).toBeLessThan(500);
    for (let i = 0; i < a.labels.length; i++)
      for (let j = i + 1; j < a.labels.length; j++)
        expect(
          Math.abs(a.labels[i].x - a.labels[j].x) >= a.width ||
            Math.abs(a.labels[i].y - a.labels[j].y) >= a.height,
        ).toBe(true);
    for (const label of a.labels) {
      const displacement = Math.abs(((label.angle - label.actual + 540) % 360) - 180);
      expect(displacement).toBeLessThanOrEqual(a.maxLabelDriftDegrees);
    }
    for (const label of a.labels)
      expect(label.actual).toBe(
        data.find((p) => p.id === label.id)!.longitude_deg,
      );
    expect(JSON.stringify(data)).toBe(saved);
  });
  it("prioritizes selection/search and increases annotation capacity with zoom", () => {
    const data = stress(500);
    const sparse = compactLabels(data, 270, "sparse", 1, null, "Object 499");
    expect(sparse.labels[0].id).toBe("asteroid-0499");
    expect(sparse.labels.length).toBeGreaterThan(0);
    expect(sparse.labels.length).toBeLessThanOrEqual(18);
    expect(
      compactLabels(data, 270, "all", 4, null, "").labels.length,
    ).toBeGreaterThan(
      compactLabels(data, 270, "all", 1, null, "").labels.length,
    );
  });
  it("renders every real marker, all six bands, exact export data and no label rectangles", () => {
    const saved = JSON.stringify(chart);
    for (const orientation of ["ascendant", "whole-sign"] as const)
      for (const density of ["sparse", "balanced", "all"] as const) {
        const svg = renderToStaticMarkup(
          <Wheel
            chart={chart}
            dual
            selected="Sun"
            onSelect={() => {}}
            precision="second"
            orientation={orientation}
            density={density}
            query=""
            zoom={1}
          />,
        );
        expect((svg.match(/data-object-id=/g) ?? []).length).toBe(
          points.length,
        );
        expect((svg.match(/data-decan-ruler=/g) ?? []).length).toBe(36);
        expect((svg.match(/data-energy-house=/g) ?? []).length).toBe(12);
        expect(svg).not.toContain("<rect");
        for (const p of points)
          expect(svg).toContain(
            `data-object-id="${p.id}" data-longitude="${p.longitude_deg}"`,
          );
        expect(svg).not.toContain("aspect");
      }
    expect(JSON.stringify(chart)).toBe(saved);
  });
  it("renders 500 markers even when only 18 labels are requested", () => {
    const dense = {
      ...chart,
      points: stress(500).map((p) => ({ ...points[0], ...p })),
    } as Chart;
    const svg = renderToStaticMarkup(
      <Wheel
        chart={dense}
        dual
        selected="asteroid-0499"
        onSelect={() => {}}
        precision="minute"
        orientation="whole-sign"
        density="sparse"
        query=""
        zoom={1}
      />,
    );
    expect((svg.match(/data-object-id=/g) ?? []).length).toBe(500);
    expect((svg.match(/data-label-id=/g) ?? []).length).toBe(18);
  });
  it("retains the original renderer as a working rollback", () => {
    const svg = renderToStaticMarkup(
      <LegacyWheel
        chart={chart}
        dual
        selected="Sun"
        onSelect={() => {}}
        precision="second"
      />,
    );
    expect((svg.match(/data-object-id=/g) ?? []).length).toBe(points.length);
    for (const p of points)
      expect(svg).toContain(
        `data-object-id="${p.id}" data-longitude="${p.longitude_deg}"`,
      );
  });
});
