import type { Point } from "./types";

/** PURE ASTROLOGY p207, p569: four Gradities; stationary Inertial Points
 * are motion transitions, NOT fifth and sixth Gradity phases.
 */
export type MotionStatus = "Direct" | "Retrograde" | "Stationary" | "Unknown";
export type GradityPhase = "Prograde" | "Pregrade" | "Retrograde" | "Postgrade";

export function motionStatus(point: Pick<Point, "speed_longitude_deg_per_day" | "retrograde">): MotionStatus {
  const speed = point.speed_longitude_deg_per_day;
  if (typeof speed === "number" && Number.isFinite(speed)) {
    if (speed === 0) return "Stationary";
    return speed < 0 ? "Retrograde" : "Direct";
  }
  if (point.retrograde === true) return "Retrograde";
  if (point.retrograde === false) return "Direct";
  return "Unknown";
}

/** A plain retrograde velocity is sufficient to identify the retrograde phase.
 * Pregrade, Postgrade and Prograde require verified exact station/boundary
 * longitudes; no guessed calendar windows or speed cutoffs are permitted.
 */
export function observedGradity(point: Pick<Point, "speed_longitude_deg_per_day" | "retrograde">): GradityPhase | null {
  return motionStatus(point) === "Retrograde" ? "Retrograde" : null;
}

/** Optional verified event inputs for future Gradeity timing. Station instants
 * and boundary crossings must be independently solved before supplying them.
 * At an exact boundary the author's equality convention is undetermined.
 */
export type VerifiedGradityCycle = {
  pregradeEntryUtc: string;
  stationRetrogradeUtc: string;
  stationDirectUtc: string;
  postgradeExitUtc: string;
  sourceStatus: "VERIFIED_ASTRONOMICAL_EVENTS";
};
export function gradityAtUtc(utc: string, cycle: VerifiedGradityCycle): GradityPhase | null {
  if (cycle.sourceStatus !== "VERIFIED_ASTRONOMICAL_EVENTS") return null;
  const stamps = [cycle.pregradeEntryUtc, cycle.stationRetrogradeUtc, cycle.stationDirectUtc, cycle.postgradeExitUtc];
  if (![utc, ...stamps].every(s => /Z$/.test(s) && Number.isFinite(Date.parse(s)))) return null;
  const [a, b, c, d] = stamps.map(Date.parse);
  const now = Date.parse(utc);
  if (!(a < b && b < c && c < d)) return null;
  if (now <= a || now === b || now === c || now >= d) return null;
  if (now < b) return "Pregrade";
  if (now < c) return "Retrograde";
  return "Postgrade";
}
