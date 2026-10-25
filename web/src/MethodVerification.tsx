import type { Chart, Point } from "./types";
import { gradityDisplay } from "./gradeity";
import "./methodVerification.css";

const names: Record<string, string> = {
  whole_sign: "Whole Sign houses",
  true_placement: "True Placement / Field",
  tone: "Astronomical sign / Tone",
  pulse: "Decan / Pulse",
  ruler: "Modern planetary rulers",
  parts: "Parts",
  nonagesimal: "Nonagesimal / Subnonagesimal",
  gradity: "Gradity",
  spark: "Spark",
  aspects: "Directional aspects",
  progressions: "Progressions",
};

function readable(value: unknown): string {
  if (typeof value === "string") return value;
  if (value == null) return "";
  return JSON.stringify(value);
}

export function MethodVerification({ rules }: { rules: Chart["rules"] }) {
  return (
    <details className="method-verification">
      <summary>Method verification</summary>
      <p>
        These statuses describe implementation of documented methods. Independent
        astronomical comparisons cover the recorded samples; method verification
        does not establish scientific evidence for an interpretation.
      </p>
      <dl>
        {Object.entries(rules).map(([key, value]) => {
          if (!value || typeof value !== "object") return null;
          const rule = value as Record<string, unknown>;
          const status = readable(rule.status);
          const statusLabel = status === "READY" ? "Implemented method" : status === "VERIFIED" ? "Verified method" : status.startsWith("VERIFIED_") ? `Method verified ${status.slice(9).replaceAll("_", " ").toLowerCase()}` : status.replaceAll("_", " ").toLowerCase();
          return (
            <div key={key}>
              <dt>{names[key] || key.replaceAll("_", " ")}</dt>
              <dd>
                <strong>{statusLabel}</strong>
                {!!rule.reason && <p>{readable(rule.reason)}</p>}
                {!!rule.evidence && <p>Source: {readable(rule.evidence)}</p>}
                {!!(rule.verification_scope || rule.scope) && <p>Scope: {readable(rule.verification_scope || rule.scope)}</p>}
                <small>{readable(rule.id)}{rule.version ? ` · rule version ${readable(rule.version)}` : ""}</small>
              </dd>
            </div>
          );
        })}
      </dl>
    </details>
  );
}

export function GradityDetails({ point }: { point: Pick<Point, "group" | "gradity" | "speed_longitude_deg_per_day" | "retrograde"> }) {
  if (!point.gradity || point.gradity.status === "NOT_APPLICABLE") return null;
  const display = gradityDisplay(point);
  return (
    <details className="gradity-details">
      <summary>Gradity calculation details</summary>
      <p>{display.reason}</p>
      {point.gradity.verification_scope && <p>Verification scope: {point.gradity.verification_scope.replaceAll("_", " ")}.</p>}
      {point.gradity.source && <p>Source: PDF page {point.gradity.source.pdf_pages?.join(", ") || "not recorded"}; original printed page {point.gradity.source.original_printed_pages?.join(", ") || "not recorded"}{point.gradity.source.reflow_pages?.length ? `; reflow page ${point.gradity.source.reflow_pages.join(", ")}` : ""}.</p>}
      {!!point.gradity.events?.length && (
        <>
          <p>Computed event records include UTC times and the solver's recorded numerical tolerances. Solver precision is separate from independent astronomical agreement and birth-time uncertainty. Boundary handling preserves an unassigned phase at an undecided exact transition.</p>
          <pre>{JSON.stringify(point.gradity.events, null, 2)}</pre>
        </>
      )}
    </details>
  );
}
