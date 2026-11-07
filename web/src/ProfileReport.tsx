import { useEffect, useRef, useState } from "react";
import { ArrowDownToLine, ArrowLeft, Printer, RefreshCw } from "lucide-react";
import type { BirthInput, Chart } from "./types";
import { Wheel } from "./Wheel";
import "./profileReport.css";
import PractitionerWorkspace from "./PractitionerWorkspace";

export type ProfileSection = {
  id: string;
  title: string;
  status: "calculated" | "source_vocabulary" | "source_context" | "unavailable";
  summary: string;
  facts: { label: string; value: string }[];
  source_refs: string[];
  rule_ids: string[];
  blockers: string[];
};
export type ProfilePacket = {
  schema_version: "nadia-profile/1";
  report_id: string;
  tier: "essential" | "premium";
  synthetic: boolean;
  profile: {
    name: string;
    birth_date: string;
    birth_time: string | null;
    location: string;
    timezone: string;
    time_accuracy: string;
  };
  chart: Chart;
  readiness: {
    technical_report_ready: boolean;
    complete_personal_reading: false;
    interpretation_status: "blocked";
    knowledge_status: "verified" | "unavailable";
    limitations: string[];
  };
  sections: ProfileSection[];
  lead: {
    question: string;
    reflection_question: string;
    personalized_answer: null;
    booking_url: string | null;
  };
  core_identity: { version: string; commit: string } | null;
  reading_guide?: {
    scope: "bounded_source_context_not_personal_synthesis";
    time_dependent_context_available: boolean;
    focus: { body: string; section_id: string; function: string; vocabulary: string;
      context: { label: string; value: string }[]; represented_houses: string[];
      question: string; question_status: "optional_reflection_not_chart_inference";
      source_refs: string[]; rule_ids: string[]; personal_inference_allowed: false }[];
  };
  review?: { status: "required"; submitted: false; personal_interpretation_approved: false;
    scope: string; requirements: string[] };
};

export function safeBookingUrl(value: string | null): string | null {
  if (!value) return null;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !url.username && !url.password
      ? url.href
      : null;
  } catch {
    return null;
  }
}

export function acceptProfilePacket(value: unknown): ProfilePacket {
  const data = value as ProfilePacket;
  if (
    !data ||
    data.schema_version !== "nadia-profile/1" ||
    data.readiness?.complete_personal_reading !== false ||
    typeof data.readiness?.technical_report_ready !== "boolean" ||
    data.readiness?.interpretation_status !== "blocked" ||
    !["verified", "unavailable"].includes(data.readiness?.knowledge_status) ||
    !Array.isArray(data.readiness?.limitations) ||
    data.lead?.personalized_answer !== null ||
    typeof data.profile?.name !== "string" ||
    !["essential", "premium"].includes(data.tier) ||
    !Array.isArray(data.sections) ||
    !data.sections.every((s) =>
      ["calculated", "source_vocabulary", "source_context", "unavailable"].includes(s.status) &&
      typeof s.title === "string" && typeof s.summary === "string" &&
      Array.isArray(s.facts) && Array.isArray(s.source_refs) &&
      Array.isArray(s.rule_ids) && Array.isArray(s.blockers),
    ) ||
    !Array.isArray(data.chart?.points)
    || (data.review !== undefined && (data.review.status !== "required" ||
      data.review.submitted !== false || data.review.personal_interpretation_approved !== false ||
      !Array.isArray(data.review.requirements)))
    || (data.reading_guide !== undefined && (data.reading_guide.scope !== "bounded_source_context_not_personal_synthesis" ||
      !Array.isArray(data.reading_guide.focus) || !data.reading_guide.focus.every(f =>
        f.personal_inference_allowed === false && f.question_status === "optional_reflection_not_chart_inference" &&
        typeof f.function === "string" && typeof f.vocabulary === "string" &&
        Array.isArray(f.context) && Array.isArray(f.represented_houses) &&
        Array.isArray(f.source_refs) && Array.isArray(f.rule_ids))))
  ) {
    throw new Error("This report could not pass its interpretation checks. Please try again.");
  }
  return data;
}

export function reviewBrief(packet: ProfilePacket): string {
  return ["NADIA — personal interpretation review required", `Report: ${packet.report_id}`,
    `Chart: ${packet.profile.name}`, `Birth: ${packet.profile.birth_date} ${packet.profile.birth_time ?? "unknown time"} (${packet.profile.timezone})`,
    `Place: ${packet.profile.location}`, `Time accuracy: ${packet.profile.time_accuracy}`,
    "", "Status: not submitted; no personal interpretation approved.",
    "The attached report JSON contains calculated facts, source dependencies and unknowns. This brief grants no authority to bypass those gates.",
    "", "Question for consultation", packet.lead.question,
    "", "Source-supported starting points",
    ...(packet.reading_guide?.focus ?? []).flatMap(f => [
      `${f.body}: ${f.function}. Source vocabulary: ${f.vocabulary}.`,
      ...f.context.map(c => `${c.label}: ${c.value}`),
      ...f.represented_houses.map(h => `Represents (not occupied placement): ${h}`),
      `Evidence: ${f.source_refs.join(", ")}`, ""]),
    "Reviewer checklist", ...(packet.review?.requirements ?? []).map(r => `[ ] ${r}`),
    "", "Unresolved conditions", ...packet.readiness.limitations.map(l => `- ${l}`),
    "", "Reviewer records separately: proposed conclusion; exact supporting facts and sources; applicability; missing conditions; judgment and confidence; disposition and reviewer identity.",
    "No review has been requested or transmitted by downloading this file. Private reflection notes are excluded.", ""].join("\n");
}

function downloadReview(packet: ProfilePacket) {
  const url = URL.createObjectURL(new Blob([reviewBrief(packet)], { type: "text/plain;charset=utf-8" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `nadia-review-${packet.report_id.slice(0, 16)}.txt`;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
}

function downloadReport(packet: ProfilePacket) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(packet, null, 2) + "\n"], { type: "application/json" }),
  );
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `nadia-profile-${packet.report_id.slice(0, 16)}.json`;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
}

function sourceLabel(ref: string) {
  return ref.startsWith("original-page-")
    ? `Original printed page ${ref.slice("original-page-".length)}`
    : ref;
}

export function compactSourceLabels(refs: string[]): string {
  const pages = [...new Set(refs.filter(r => /^original-page-\d+$/.test(r)).map(r => Number(r.slice(14))))].sort((a, b) => a - b);
  const spans: string[] = [];
  for (let i = 0; i < pages.length; i++) {
    const start = pages[i];
    while (i + 1 < pages.length && pages[i + 1] === pages[i] + 1) i++;
    spans.push(start === pages[i] ? String(start) : `${start}–${pages[i]}`);
  }
  return [pages.length ? `Original printed pages ${spans.join(", ")}` : "", ...refs.filter(r => !/^original-page-\d+$/.test(r))].filter(Boolean).join("; ");
}

export type ReviewedSection = { id: string; question: string; claims: {
  part: string; text: string; basis: string; practice_kind: string; source_refs: string[];
  review: { actor: string; scope?: string };
}[] };

export function ReportContents({ packet, individualReview }: { packet: ProfilePacket;
  individualReview?: { reviewed_sections: ReviewedSection[]; demonstration: boolean; incomplete_questions: string[]; case_id: string; revision: number } }) {
  const [selected, setSelected] = useState<string | null>(null);
  const [reflection, setReflection] = useState("");
  const booking = safeBookingUrl(packet.lead.booking_url);
  const available = packet.sections.filter((s) => s.status !== "unavailable" && s.status !== "source_vocabulary");
  return (
    <article className={`nadia-report-document${individualReview ? " nadia-reviewed-report" : ""}`} aria-label="NADIA profile report">
      {individualReview?.demonstration && <p className="nadia-workflow-demo">Workflow demonstration - example content, not an expert reading. Internal review only.</p>}
      <header className="nadia-report-cover">
        <div className="nadia-report-cover-copy">
          <p className="nadia-wordmark">NADIA<span className="nadia-print-report-id"> · {packet.report_id.slice(0, 16)}</span></p>
          <p className="nadia-report-edition">Your chart profile</p>
          <h1>{packet.profile.name}</h1>
          <p className="nadia-report-subtitle">A map to explore. A conversation to make it personal.</p>
          {packet.synthetic && <p className="nadia-synthetic">Synthetic demonstration · not a real person's reading</p>}
          {!packet.readiness.technical_report_ready && <p className="nadia-synthetic">Some required chart positions are unavailable. This document contains the available facts only.</p>}
        </div>
        <dl className="nadia-birth-summary">
          <div><dt>Birth date</dt><dd>{packet.profile.birth_date}</dd></div>
          <div><dt>Birth time</dt><dd>{packet.profile.birth_time ?? "Unknown — time-dependent results withheld"}</dd></div>
          <div><dt>Birth-time precision</dt><dd>{packet.profile.time_accuracy.replaceAll("_", " ")}{packet.chart.time.uncertainty_seconds != null ? `; ±${packet.chart.time.uncertainty_seconds} seconds` : ""}</dd></div>
          <div><dt>Birthplace</dt><dd>{packet.profile.location}</dd></div>
          <div><dt>Time zone</dt><dd>{packet.profile.timezone}</dd></div>
        </dl>
      </header>

      <section className="nadia-report-introduction">
        <h2>Read your chart with confidence</h2>
        <p>{individualReview ? "This profile combines your calculated chart with individually reviewed sections. Review applies to those sections alone; it does not authorize automated personal interpretation or establish a complete profile. Unfinished questions are left incomplete." : "This profile brings together your calculated placements and the source-supported context available for them. Complete personal interpretation is not yet available. Personal conclusions require qualified review; this document does not diagnose, predict events or infer your history."}</p>
        <div className="nadia-reading-key" aria-label="Report scope"><span>Calculated placements</span><span>Bounded source context</span><span>{individualReview ? "Individual review provenance retained" : "Personal interpretation: review required"}</span></div>
      </section>

      {individualReview?.reviewed_sections.map(section => <section className="nadia-individual-insights" key={section.id}>
        <h2>{section.question}</h2>{section.claims.map(c => <div key={c.part}>
          <h3>{c.part === "recognition" ? "Recognition" : c.part === "explanation" ? "Explanation" : "Practical application"}</h3><p>{c.text}</p>
          <p className="nadia-manual-provenance">{individualReview.demonstration ? "Demonstration content" : c.basis === "expert_judgment" ? "Practitioner judgment" : "Source-supported interpretation assessed by practitioner"} · reviewed by {c.review.actor} for this case only.{c.part === "practical_application" ? c.practice_kind === "adaptation" ? " New adaptation." : " Sourced practice; applicability individually reviewed." : ""}{c.source_refs.length > 0 ? ` References: ${compactSourceLabels(c.source_refs)}.` : ""}</p>
        </div>)}
      </section>)}
      {individualReview && <section className="nadia-report-introduction nadia-incomplete-questions"><h2>Questions still to explore</h2><ul>{individualReview.incomplete_questions.map(q => <li key={q}>{q}</li>)}</ul><p>No interpretation has been supplied for these questions. Review record {individualReview.case_id.slice(0, 12)}, revision {individualReview.revision}. The separate private evidence record retains reasoning, limits and review decisions.</p></section>}

      <section className="nadia-report-chart" aria-labelledby="profile-chart-heading">
        <div className="nadia-report-chart-copy">
          <h2 id="profile-chart-heading">The chart behind this profile</h2>
          <p>Tropical, geocentric positions with Whole Sign houses where birth-time precision permits. Field, Tone and Pulse are shown as calculated layers.</p>
          <p>These layers need their full configuration and related context before a personal conclusion can be drawn.</p>
          <p className="nadia-chart-caption">Select a planet to inspect its position on the chart.</p>
          <label className="nadia-chart-picker">Inspect chart object
            <select aria-label="Inspect chart object" value={selected ?? ""} onChange={event => setSelected(event.target.value || null)}>
              <option value="">Choose an object</option>
              {packet.chart.points.filter(point => point.available).map(point => <option key={point.id} value={point.id}>{point.name}</option>)}
            </select>
          </label>
        </div>
        <div className="nadia-report-wheel">
          <Wheel chart={packet.chart} dual={false} selected={selected} onSelect={setSelected} precision="second" orientation="ascendant" density="balanced" query="" zoom={1} />
        </div>
      </section>

      <section className="nadia-profile-overview" aria-labelledby="profile-overview-heading">
        <h2 id="profile-overview-heading">Your chart at a glance</h2>
        <p>Each row describes a position, not a personality verdict. House is the occupied life area; a planet can represent other houses through rulership.</p>
        <table className="nadia-placement-table"><thead><tr><th scope="col">Planet</th><th scope="col">Position</th><th scope="col">House</th><th scope="col">Own motion</th></tr></thead>
          <tbody>{packet.chart.points.filter(p => p.available && p.group !== "angles" && !["Ascendant", "Midheaven"].includes(p.id)).map(p =>
            <tr key={p.id}><th scope="row">{p.name}</th><td>{p.display_dms}</td><td>{p.house ?? "Withheld"}</td><td>{p.retrograde === null ? "Unknown" : p.retrograde ? "Retrograde" : "Direct"}</td></tr>)}</tbody></table>
        {!packet.reading_guide?.time_dependent_context_available && <p className="nadia-component-limit">Time-dependent context is withheld when the birth time is missing or uncertain.</p>}
      </section>

      {packet.sections.filter(s => s.id === "relationships-graph" && s.status === "source_context").map(s => <section className="nadia-profile-connections" key={s.id}>
        <h2>Verified connections</h2><p>{s.summary}</p>
        <dl className="nadia-report-facts">{s.facts.map((f, i) => <div key={i}><dt>{f.label}</dt><dd>{f.value}</dd></div>)}</dl>
        <p className="nadia-method-note">The sending planet contributes to the receiving planet’s context. An arrow establishes direction, not whether the experience is helpful or difficult. The full participant meanings and conditions still need review.</p>
        <p className="nadia-focus-source">Source: {compactSourceLabels(s.source_refs)}</p>
      </section>)}

      {!!packet.reading_guide?.focus.length && <section className="nadia-profile-focus" aria-labelledby="profile-focus-heading">
        <h2 id="profile-focus-heading">Expression & emotional security</h2>
        <p className="nadia-focus-intro">Two starting points for understanding the method. The source gives each planet a function; its placement supplies context. Their combined personal meaning still needs assessment.</p>
        <div className="nadia-focus-columns">{packet.reading_guide.focus.map(f => <section key={f.body} className="nadia-focus-item">
          <h3>{f.body}</h3><p className="nadia-focus-function">{f.function}</p><p>{f.vocabulary}</p>
          <dl className="nadia-report-facts">{f.context.map(c => <div key={c.label}><dt>{c.label}</dt><dd>{c.value}</dd></div>)}</dl>
          {f.represented_houses.length > 0 && <div className="nadia-represented"><h4>Houses this planet represents</h4>{f.represented_houses.map(h => <p key={h}>{h}</p>)}<p>These are rulership links, not additional occupied placements.</p></div>}
          <p className="nadia-reflection-prompt">For reflection, not inferred from your chart: {f.question}</p>
          <p className="nadia-focus-source">Source: {compactSourceLabels(f.source_refs)}</p>
        </section>)}</div>
        <p className="nadia-method-note">Field describes the house context, Tone the sign layer, and Pulse the calculated degree layer. A label alone does not establish its contextual effect. Follow the ruler and verified contacts in the appendix before proposing a personal conclusion.</p>
      </section>}



      <section className="nadia-profile-review" aria-labelledby="profile-review-heading">
        <div><p className="nadia-review-status">Personal interpretation · review required</p><h2 id="profile-review-heading">Make the next conversation useful</h2>
        <p>Your chart cannot tell us which experiences you have actually had. Bring your own examples; a reviewer can assess how the supported configuration relates to your question.</p></div>
        <div><ol>{(packet.review?.requirements ?? ["Check the birth details.", "Review personal interpretations against the source and full configuration."]).map(r => <li key={r}>{r}</li>)}</ol>
        <p className="nadia-print-review-question">Question for review: {packet.lead.question}</p>
        <div className="nadia-print-notes"><h3>Notes to bring to your consultation</h3><p>Use this space for your own experiences and questions. These are not conclusions from your chart.</p>{Array.from({ length: 6 }, (_, i) => <div key={i} />)}</div>
        <button type="button" className="nadia-review-download" onClick={() => downloadReview(packet)}><ArrowDownToLine size={17} />Download review brief</button>
        <p className="nadia-review-note">Downloads a local checklist. Nothing is submitted. Share it with the report JSON only when you choose. Review cannot override an unresolved source rule.</p></div>
      </section>



      <details className="nadia-technical-appendix">
      <summary>Supporting appendix: calculated chart context</summary>
      <section className="nadia-report-available" aria-labelledby="profile-components-heading">
        <div className="nadia-section-intro">
          <h2 id="profile-components-heading">Supporting chart context</h2>
          <p>These calculations support methodology review. They are not personal conclusions.</p>
        </div>
        {available.map((section) => (
          <section key={section.id} id={`profile-${section.id}`} className="nadia-report-section" data-profile-section={section.id}>
            <div className="nadia-section-heading">
              <h3>{section.title}</h3>
              <span className="nadia-section-status">{section.status === "calculated" ? "Calculated facts" : section.status === "source_context" ? "Scoped source context" : "Source vocabulary"}</span>
            </div>
            <p>{section.summary}</p>
            {section.facts.length > 0 && <dl className="nadia-report-facts">{section.facts.map((fact, index) => <div key={`${fact.label}-${index}`}><dt>{fact.label}</dt><dd>{fact.value}</dd></div>)}</dl>}
            {section.source_refs.length > 0 && <><details className="nadia-section-evidence"><summary>Source evidence</summary><ul>{section.source_refs.map((ref) => <li key={ref}>{sourceLabel(ref)}</li>)}</ul><p>These references support this component's stated scope. They do not certify a complete personal reading.</p></details><p className="nadia-print-sources">Source: {compactSourceLabels(section.source_refs)}</p></>}
          </section>
        ))}
      </section>
      </details>

      <section className="nadia-report-consultation" aria-labelledby="profile-love-heading">
        <div><p className="nadia-consultation-label">A question to bring to your reading</p><h2 id="profile-love-heading">{packet.lead.question}</h2><p>Your own experience is a useful starting point for a conversation.</p></div>
        <div className="nadia-reflection">
          <label htmlFor="profile-reflection">{packet.lead.reflection_question}</label>
          <textarea id="profile-reflection" rows={4} maxLength={2000} value={reflection} onChange={(event) => setReflection(event.target.value)} placeholder="Write a note for yourself…" />
          <p className="nadia-reflection-privacy">This note stays in this view. It is not sent, saved or included in the report export.</p>
          {booking ? <a className="nadia-booking" href={booking} target="_blank" rel="noopener noreferrer">Explore a full consultation</a> : <p className="nadia-booking-pending">A booking destination has not been connected yet.</p>}
        </div>
      </section>
      <footer className="nadia-report-footer"><span>NADIA · {packet.synthetic ? "Synthetic demonstration" : "Private profile"}</span><span>Bounded chart profile · personal interpretation requires review</span><span>Report {packet.report_id.slice(0, 16)}</span></footer>
    </article>
  );
}

export default function ProfileReport({ birth, synthetic, onClose }: { birth: BirthInput; synthetic: boolean; onClose: () => void }) {
  const tier = "essential";
  const [packet, setPacket] = useState<ProfilePacket | null>(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const sequence = useRef(0);
  const [workspace, setWorkspace] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    const current = ++sequence.current;
    setBusy(true);
    setError("");
    setPacket(null);
    void fetch("/api/profile-reports", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birth, tier, synthetic }),
      signal: controller.signal,
      cache: "no-store",
    }).then(async (response) => {
      const result = await response.json();
      if (!response.ok) throw new Error(result.error?.message ?? "The profile could not be generated. Please check your birth details and try again.");
      const report = acceptProfilePacket(result);
      if (current === sequence.current && !controller.signal.aborted) setPacket(report);
    }).catch((reason: unknown) => {
      if (current === sequence.current && !controller.signal.aborted) setError(reason instanceof Error ? reason.message : "The profile service could not be reached. Please try again.");
    }).finally(() => {
      if (current === sequence.current && !controller.signal.aborted) setBusy(false);
    });
    return () => controller.abort();
  }, [birth, tier, synthetic, attempt]);

  if (workspace) return <PractitionerWorkspace birth={birth} synthetic={synthetic} onClose={() => setWorkspace(false)} />;
  return <div className="nadia-report-app">
    <nav className="nadia-report-toolbar" aria-label="Profile report controls">
      <button type="button" onClick={onClose}><ArrowLeft size={17} />Back to chart</button>
      <span>Chart profile</span>
      <button type="button" onClick={() => setWorkspace(true)}>Practitioner workspace</button>
      <div className="nadia-report-export"><button type="button" disabled={!packet || busy} onClick={() => packet && downloadReport(packet)}><ArrowDownToLine size={17} />Download JSON</button><button type="button" disabled={!packet || busy} onClick={() => window.print()}><Printer size={17} />Print / save PDF</button></div>
    </nav>
    {busy && <div className="nadia-report-loading" role="status"><p className="nadia-wordmark">NADIA</p><h1>Preparing your profile</h1><p>Calculating the chart and checking which components can be shown.</p></div>}
    {error && <div className="nadia-report-loading" role="alert"><h1>The profile needs another look</h1><p>{error}</p><button type="button" onClick={() => setAttempt((n) => n + 1)}><RefreshCw size={17} />Try again</button></div>}
    {packet && !busy && <ReportContents key={packet.report_id} packet={packet} />}
    <p className="nadia-report-privacy">Birth details and the generated report are handled in memory for this request. Downloaded files may contain sensitive personal information.</p>
  </div>;
}
