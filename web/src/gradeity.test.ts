import { describe, it, expect } from "vitest";
import { gradityAtUtc, gradityDisplay, motionStatus, observedGradity, type VerifiedGradityCycle } from "./gradeity";

// Source PDF203/reflow207/original143 and PDF477/original569: four Gradities.
const cycle: VerifiedGradityCycle = {
  pregradeEntryUtc: "2026-10-01T00:00:00Z",
  stationRetrogradeUtc: "2026-10-10T00:00:00Z",
  stationDirectUtc: "2026-11-10T00:00:00Z",
  postgradeExitUtc: "2026-11-24T00:00:00Z",
  sourceStatus: "VERIFIED_ASTRONOMICAL_EVENTS",
};
describe("book-constrained Gradity states", () => {
  it("separates motion state from four Gradity phases", () => {
    expect(motionStatus({ speed_longitude_deg_per_day: -0.02, retrograde: true })).toBe("Retrograde");
    expect(motionStatus({ speed_longitude_deg_per_day: 0.02, retrograde: false })).toBe("Direct");
    expect(motionStatus({ speed_longitude_deg_per_day: 0, retrograde: false })).toBe("Stationary");
    expect(motionStatus({ retrograde: null })).toBe("Unknown");
    expect(observedGradity({ speed_longitude_deg_per_day: -0.02, retrograde: true })).toBe("Retrograde");
    expect(observedGradity({ speed_longitude_deg_per_day: 0.02, retrograde: false })).toBeNull();
  });
  it("requires verified crossings before assigning pregrade or postgrade", () => {
    expect(gradityAtUtc("2026-10-05T00:00:00Z", cycle)).toBe("Pregrade");
    expect(gradityAtUtc("2026-10-15T00:00:00Z", cycle)).toBe("Retrograde");
    expect(gradityAtUtc("2026-11-18T00:00:00Z", cycle)).toBe("Postgrade");
    expect(gradityAtUtc("2026-09-29T00:00:00Z", cycle)).toBeNull();
    expect(gradityAtUtc("2026-11-26T00:00:00Z", cycle)).toBeNull();
  });
  it("does not guess at exact station or boundary timestamps", () => {
    for (const utc of [cycle.pregradeEntryUtc,cycle.stationRetrogradeUtc,cycle.stationDirectUtc,cycle.postgradeExitUtc])
      expect(gradityAtUtc(utc, cycle)).toBeNull();
  });
  it("rejects impossible chronology", () => {
    expect(gradityAtUtc("2026-10-15T00:00:00Z", {...cycle, stationRetrogradeUtc: "2026-09-01T00:00:00Z"})).toBeNull();
    expect(gradityAtUtc("2026-10-15T00:00:00Z", {...cycle, sourceStatus: "NOT_VERIFIED" as VerifiedGradityCycle["sourceStatus"]})).toBeNull();
  });
  it("uses verified server phases and does not infer a loop from forward speed", () => {
    const point = { group: "Planets", speed_longitude_deg_per_day: 0.02, retrograde: false };
    for (const phase of ["Prograde", "Pregrade", "Retrograde", "Postgrade"] as const) {
      expect(gradityDisplay({ ...point, gradity: { phase, status: "VERIFIED", reason: "Computed events." } })).toEqual({ label: phase, reason: "Computed events." });
    }
    expect(gradityDisplay(point).label).toBe("Unverified");
    expect(gradityDisplay({ ...point, speed_longitude_deg_per_day: -0.02 }).label).toBe("Retrograde");
  });
  it("keeps unassigned boundaries, unavailable event data and mathematical points distinct", () => {
    const point = { group: "Planets", speed_longitude_deg_per_day: 0, retrograde: false };
    expect(gradityDisplay({ ...point, gradity: { phase: null, status: "BOUNDARY", reason: "Equality is unresolved." } })).toEqual({ label: "Boundary", reason: "Equality is unresolved." });
    expect(gradityDisplay({ ...point, speed_longitude_deg_per_day: -0.000001, gradity: { phase: null, status: "BOUNDARY", reason: "Equality is unresolved." } }).label).toBe("Boundary");
    const unavailable = { ...point, gradity: { phase: null, status: "UNAVAILABLE" as const, reason: "Search range ended." } };
    expect(gradityDisplay(unavailable).label).toBe("Unverified");
    expect(gradityDisplay({ ...unavailable, speed_longitude_deg_per_day: -0.02 })).toEqual({ label: "Retrograde", reason: "Observed retrograde from signed motion; full station/crossing classification is unavailable. Search range ended." });
    for (const group of ["Angles", "Parts", "Lunar points"]) {
      expect(gradityDisplay({ ...point, group }).label).toBe("—");
      expect(gradityDisplay({ ...point, group, gradity: { phase: "Pregrade", status: "VERIFIED", reason: "Invalid input." } }).label).toBe("—");
    }
    expect(gradityDisplay({ ...point, gradity: { phase: null, status: "NOT_APPLICABLE", reason: "No loop applicability." } }).label).toBe("—");
  });
  it("does not mutate old chart data when displaying its limited observed phase", () => {
    const point = Object.freeze({ group: "Asteroids", speed_longitude_deg_per_day: -0.02, retrograde: true });
    expect(gradityDisplay(point).label).toBe("Retrograde");
    expect(Object.keys(point)).toEqual(["group", "speed_longitude_deg_per_day", "retrograde"]);
  });
});
