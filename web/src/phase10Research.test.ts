import { describe, it, expect } from "vitest";
import { approachingFusionCusps, exactIntegerDegreeAgeLabels, sparkParityResearchCandidates } from "./phase10Research";
describe("Phase 10 source-grounded limited research helpers", () => {
  it("reproduces printed FCA thresholds independently at three scales", () => {
    const hit = approachingFusionCusps(10 + 57 / 60);
    expect(hit[2].inside_approaching).toBe(true); // 3 arcminutes before next degree
    expect(hit[2].width_degrees).toBe(0.05);
    expect(approachingFusionCusps(5 + 56 / 60)[2].inside_approaching).toBe(false); // 4 arcminutes
    expect(approachingFusionCusps(29)[0].inside_approaching).toBe(true); // one degree before next sign
    expect(approachingFusionCusps(9.6)[1].inside_approaching).toBe(true); // 24 minutes
    expect(hit.every(i => i.after_boundary_strength === null)).toBe(true);
  });
  it("keeps source-illustrated 30 year cycle as undated age labels", () => {
    expect(exactIntegerDegreeAgeLabels(2)?.ages).toEqual([2,32,62,92]);
    expect(exactIntegerDegreeAgeLabels(2)?.calendar_dates).toBeNull();
    expect(exactIntegerDegreeAgeLabels(2.5)).toBeNull();
  });
  it("preserves house-versus-sign Spark contradictions, never selects canonical", () => {
    expect(sparkParityResearchCandidates(14,10,3)).toEqual({house_parity_index:8,sign_parity_index:2,canonical:null,source_status:"CONTRADICTED"});
    expect(sparkParityResearchCandidates(10,10,1)).toEqual({house_parity_index:4,sign_parity_index:10,canonical:null,source_status:"CONTRADICTED"});
  });
});
