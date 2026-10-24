import { normalize } from "./geometry";

/** PURE ASTROLOGY Dynamic Chart Approach, printed pp507–512.
 * Approaching Fusion Cusp Areas are 5% of sign, decan and degree widths.
 * These are proximity diagnostics only, NEVER altered sign/house/Spark labels.
 */
export type FcaScale = "sign" | "decan" | "degree";
export type ApproachingFca = {
  scale: FcaScale;
  width_degrees: number;
  forward_distance_degrees: number;
  inside_approaching: boolean;
  after_boundary_strength: null;
  status: "RESEARCH_ONLY";
};
export function approachingFusionCusps(longitude: number): ApproachingFca[] {
  if (!Number.isFinite(longitude)) throw new Error("Invalid ecliptic longitude");
  const raw = normalize(longitude);
  const rules: [FcaScale, number, number][] = [
    ["sign", 30, 1.5],
    ["decan", 10, 0.5],
    ["degree", 1, 0.05],
  ];
  return rules.map(([scale, interval, width]) => {
    const position = raw % interval;
    const forward = interval - position;
    return {
      scale,
      width_degrees: width,
      forward_distance_degrees: forward,
      inside_approaching: forward > 0 && forward <= width + 1e-12,
      after_boundary_strength: null,
      status: "RESEARCH_ONLY",
    };
  });
}

/** Source p255 illustrates integer degree 2 at approximate age labels
 * 2, 32, 62, 92. For fractional degree, time/date mapping is unresolved.
 */
export function exactIntegerDegreeAgeLabels(degreeWithinSign: number, count = 4) {
  if (!Number.isInteger(degreeWithinSign) || degreeWithinSign < 0 || degreeWithinSign >= 30 || count < 1 || count > 20 || !Number.isInteger(count))
    return null;
  return { ages: Array.from({ length: count }, (_, k) => degreeWithinSign + 30 * k), precision: "AGE_LABEL_ONLY" as const, source_status: "DERIVED" as const, calendar_dates: null };
}

/** Both rules remain mathematical candidates, not a source-approved Spark.
 * House rule is explicit in Degree Theory; worked examples contradict it.
 */
export function sparkParityResearchCandidates(degreeWithinSign: number, house: number, astronomicalSign: number) {
  if (![degreeWithinSign, house, astronomicalSign].every(Number.isInteger) || degreeWithinSign < 0 || degreeWithinSign > 29 || house < 1 || house > 12 || astronomicalSign < 1 || astronomicalSign > 12)
    return null;
  const H = (degreeWithinSign + (house % 2 === 0 ? 6 : 0)) % 12;
  const Z = (degreeWithinSign + (astronomicalSign % 2 === 0 ? 6 : 0)) % 12;
  return { house_parity_index: H, sign_parity_index: Z, canonical: null, source_status: "CONTRADICTED" as const };
}
