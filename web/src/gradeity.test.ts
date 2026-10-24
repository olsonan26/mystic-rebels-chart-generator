import { describe, it, expect } from "vitest";
import { gradityAtUtc, motionStatus, observedGradity, type VerifiedGradityCycle } from "./gradeity";

// Logan, PURE ASTROLOGY printed pp207 and 569: four Gradities.
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
});
