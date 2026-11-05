import { useEffect, useRef, useState } from "react";
import { ArrowDownToLine, ArrowLeft, Printer, RefreshCw } from "lucide-react";
import type { BirthInput, Chart } from "./types";
import { Wheel } from "./Wheel";
import "./profileReport.css";

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
  ) {
    throw new Error("This report could not pass its interpretation checks. Please try again.");
  }
  return data;
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

export function ReportContents({ packet }: { packet: ProfilePacket }) {
  const [selected, setSelected] = useState<string | null>(null);
  const [reflection, setReflection] = useState("");
  const booking = safeBookingUrl(packet.lead.booking_url);
  const available = packet.sections.filter((s) => s.status !== "unavailable");
  const unavailable = packet.sections.filter((s) => s.status === "unavailable");
  return (
    <article className="nadia-report-document" aria-label="NADIA profile report">
      <header className="nadia-report-cover">
        <div className="nadia-report-cover-copy">
          <p className="nadia-wordmark">NADIA</p>
          <p className="nadia-report-edition">{packet.tier === "premium" ? "Premium profile" : "Essential profile"}</p>
          <h1>{packet.profile.name}</h1>
          <p className="nadia-report-subtitle">A considered view of your natal chart.</p>
          <p className="nadia-report-scope">Calculated chart facts and available source-backed components. Complete personal interpretation is not yet available.</p>
          {packet.synthetic && <p className="nadia-synthetic">Synthetic demonstration · not a real person's reading</p>}
          {!packet.readiness.technical_report_ready && <p className="nadia-synthetic">Some required chart positions are unavailable. This document contains the available facts only.</p>}
        </div>
        <dl className="nadia-birth-summary">
          <div><dt>Birth date</dt><dd>{packet.profile.birth_date}</dd></div>
          <div><dt>Birth time</dt><dd>{packet.profile.birth_time ?? "Unknown — time-dependent results withheld"}</dd></div>
          <div><dt>Birthplace</dt><dd>{packet.profile.location}</dd></div>
          <div><dt>Time zone</dt><dd>{packet.profile.timezone}</dd></div>
        </dl>
      </header>

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

      <section className="nadia-report-available" aria-labelledby="profile-components-heading">
        <div className="nadia-section-intro">
          <h2 id="profile-components-heading">What this profile can show</h2>
          <p>Chart facts and source vocabulary have different scopes. Each section identifies which is available.</p>
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
            {section.blockers.length > 0 && <p className="nadia-component-limit">Further interpretation remains unavailable.</p>}
          </section>
        ))}
      </section>

      <section className="nadia-report-unavailable" aria-labelledby="profile-unavailable-heading">
        <div className="nadia-section-intro">
          <h2 id="profile-unavailable-heading">What still needs a complete interpretation</h2>
          <p>These sections remain visible so that a chart summary cannot be mistaken for a comprehensive natal profile.</p>
        </div>
        <div className="nadia-unavailable-list">{unavailable.map((section) => <section key={section.id} data-profile-section={section.id}><h3>{section.title}</h3><p>{section.summary}</p><span>Interpretation unavailable</span></section>)}</div>
        <details className="nadia-section-evidence"><summary>Current profile limitations</summary><ul>{packet.readiness.limitations.map((item, index) => <li key={index}>{item}</li>)}</ul></details>
        {packet.tier === "premium" && <p className="nadia-premium-note">The premium structure is prepared for deeper verified connections. It currently includes the same approved interpretation scope as Essential.</p>}
      </section>

      <section className="nadia-report-consultation" aria-labelledby="profile-love-heading">
        <div><p className="nadia-consultation-label">A question to bring to your reading</p><h2 id="profile-love-heading">{packet.lead.question}</h2><p>This profile does not yet have a verified personalized answer to that question. Your own experience is a useful starting point for a conversation.</p></div>
        <div className="nadia-reflection">
          <label htmlFor="profile-reflection">{packet.lead.reflection_question}</label>
          <textarea id="profile-reflection" rows={4} maxLength={2000} value={reflection} onChange={(event) => setReflection(event.target.value)} placeholder="Write a note for yourself…" />
          <p className="nadia-reflection-privacy">This note stays in this view. It is not sent, saved or included in the report export.</p>
          {booking ? <a className="nadia-booking" href={booking} target="_blank" rel="noopener noreferrer">Explore a full consultation</a> : <p className="nadia-booking-pending">A booking destination has not been connected yet.</p>}
        </div>
      </section>
      <footer className="nadia-report-footer"><span>NADIA · {packet.synthetic ? "Synthetic demonstration" : "Private profile"}</span><span>Evidence-limited profile · Complete reading unavailable</span><span>Report {packet.report_id.slice(0, 16)}</span></footer>
    </article>
  );
}

export default function ProfileReport({ birth, synthetic, onClose }: { birth: BirthInput; synthetic: boolean; onClose: () => void }) {
  const [tier, setTier] = useState<"essential" | "premium">("essential");
  const [packet, setPacket] = useState<ProfilePacket | null>(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const sequence = useRef(0);
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

  return <div className="nadia-report-app">
    <nav className="nadia-report-toolbar" aria-label="Profile report controls">
      <button type="button" onClick={onClose}><ArrowLeft size={17} />Back to chart</button>
      <div className="nadia-tier-control"><label htmlFor="profile-tier">Profile</label><select id="profile-tier" value={tier} onChange={(event) => setTier(event.target.value as "essential" | "premium")}><option value="essential">Essential</option><option value="premium">Premium</option></select></div>
      <div className="nadia-report-export"><button type="button" disabled={!packet || busy} onClick={() => packet && downloadReport(packet)}><ArrowDownToLine size={17} />Download JSON</button><button type="button" disabled={!packet || busy} onClick={() => window.print()}><Printer size={17} />Print / save PDF</button></div>
    </nav>
    {busy && <div className="nadia-report-loading" role="status"><p className="nadia-wordmark">NADIA</p><h1>Preparing your profile</h1><p>Calculating the chart and checking which components can be shown.</p></div>}
    {error && <div className="nadia-report-loading" role="alert"><h1>The profile needs another look</h1><p>{error}</p><button type="button" onClick={() => setAttempt((n) => n + 1)}><RefreshCw size={17} />Try again</button></div>}
    {packet && !busy && <ReportContents key={packet.report_id} packet={packet} />}
    <p className="nadia-report-privacy">Birth details and the generated report are handled in memory for this request. Downloaded files may contain sensitive personal information.</p>
  </div>;
}
