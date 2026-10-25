import type { Point } from "./types";

/** Source PDF203 / reflow207 / original143; PDF477 / original569:
 * four Gradities; stationary Inertial Points
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

/** Render the same scoped method result in the inspector and position table.
 * Saved charts from before the event solver can establish observed retrograde
 * motion only; their forward motion must not invent an uncomputed loop phase.
 */
export function gradityDisplay(point: Pick<Point, "group" | "gradity" | "speed_longitude_deg_per_day" | "retrograde">) {
  if (!["Planets", "Asteroids", "Minor bodies"].includes(point.group) || point.gradity?.status === "NOT_APPLICABLE") {
    return { label: "—", reason: point.gradity?.reason || "Planetary Gradity does not apply to this mathematical point." };
  }
  const result = point.gradity;
  if (result?.status === "VERIFIED" && ["Prograde", "Pregrade", "Retrograde", "Postgrade"].includes(result.phase ?? "")) {
    return { label: result.phase!, reason: result.reason };
  }
  if (result?.status === "BOUNDARY") {
    return { label: "Boundary", reason: result.reason || "The exact station or crossing has no source-established phase assignment." };
  }
  if (result?.status === "UNAVAILABLE" && observedGradity(point) === "Retrograde") {
    return { label: "Retrograde", reason: `Observed retrograde from signed motion; full station/crossing classification is unavailable. ${result.reason}` };
  }
  if (result) {
    return { label: "Unverified", reason: result.reason || "The required station and crossing events have not been established." };
  }
  const observed = observedGradity(point);
  return observed
    ? { label: observed, reason: "Observed retrograde motion; this older chart has no computed station or crossing events." }
    : { label: "Unverified", reason: "This older chart has no computed station or crossing events. Recalculate it to check Gradity." };
}

/** Retained standalone classifier for externally verified event inputs. Station instants
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
