import { useEffect, useState } from "react";
import type { BirthInput } from "./types";
import { ReportContents, type ProfilePacket, type ReviewedSection } from "./ProfileReport";
import "./practitioner.css";

type Part = "recognition" | "explanation" | "practical_application";
type Claim = {
  id: string | null; question_id: string; part: Part; text: string;
  basis: "source_supported" | "expert_judgment" | "example_content";
  evidence_ids: string[]; source_refs: string[]; rationale: string;
  limitations: string; rejected_alternative: string;
  practice_kind: "not_applicable" | "source_practice" | "adaptation";
  status?: string; review?: { actor: string; note: string } | null;
};
type Case = {
  id: string; revision: number; packet: ProfilePacket; demonstration: boolean;
  questions: Record<string, string>; claims: Claim[];
  preparation: {
    evidence: Record<string, { kind: string; label: string; value: unknown }>;
    source_refs: string[]; relationships: unknown; bounded_suggestions: { theme: string | null; blockers: string[] }[];
    missing: string[]; selection: string;
  };
};
type Session = { actor: string; csrf: string };
type Assembled = { packet: ProfilePacket; reviewed_sections: ReviewedSection[]; demonstration: boolean;
  incomplete_questions: string[]; case_id: string; revision: number };
type References = { strongest_reference?: { question: string; final_expert_conclusion: { text: string };
  intermediate_states: { id: string; meaning: string }[]; missing_reasoning: string[] };
  source_media?: { id: string }[] };
const parts: Part[] = ["recognition", "explanation", "practical_application"];
const questionOrder = ["identity", "strengths", "challenges", "motivation", "talents", "relationships", "family", "application", "love"];
const partLabel = { recognition: "Recognition", explanation: "Explanation", practical_application: "Practical application" };
function editable(c: Claim): Claim {
  const { id, question_id, part, text, basis, evidence_ids, source_refs, rationale, limitations, rejected_alternative, practice_kind } = c;
  return { id, question_id, part, text, basis, evidence_ids, source_refs, rationale, limitations, rejected_alternative, practice_kind };
}
function saveFile(name: string, data: unknown) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
  const a = document.createElement("a"); a.href = url; a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
}

function EvidencePreview({ value }: { value: unknown }) {
  const record = value as Record<string, unknown>;
  const facts = Array.isArray(record.facts) ? record.facts as { label: string; value: string }[] : null;
  if (facts) return <dl className="review-fact-summary">{facts.map((f, i) => <div key={i}><dt>{f.label}</dt><dd>{f.value}</dd></div>)}</dl>;
  const placement = (record.placement ?? record) as Record<string, unknown>;
  const rows = [["Source function", record.function], ["Position", record.display_dms],
    ["Occupied house", placement.house], ["Field", placement.field], ["Tone", placement.tone], ["Pulse", placement.pulse],
    ["Own motion", typeof record.retrograde === "boolean" ? record.retrograde ? "Retrograde" : "Direct" : null]];
  return <dl className="review-fact-summary">{rows.filter(([,v]) => v != null).map(([k,v]) => <div key={String(k)}><dt>{String(k)}</dt><dd>{String(v)}</dd></div>)}</dl>;
}

export default function PractitionerWorkspace({ birth, synthetic, onClose }: {
  birth: BirthInput; synthetic: boolean; onClose: () => void;
}) {
  const [session, setSession] = useState<Session | null>(null);
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false); const [demo, setDemo] = useState(true);
  const [current, setCurrent] = useState<Case | null>(null);
  const [savedCases, setSavedCases] = useState<{ id: string; name: string; revision: number; demonstration: boolean }[]>([]);
  const [question, setQuestion] = useState("love"); const [draft, setDraft] = useState<Claim[]>([]);
  const [dirty, setDirty] = useState(false);
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [checks, setChecks] = useState<Record<string, boolean>>({});
  const [assembled, setAssembled] = useState<Assembled | null>(null);
  const [history, setHistory] = useState<unknown>(null);
  const [references, setReferences] = useState<References | null>(null);
  const [consent, setConsent] = useState("");
  const [feedback, setFeedback] = useState("");
  const [voluntary, setVoluntary] = useState(false);
  const [feedbackRole, setFeedbackRole] = useState("reader");
  useEffect(() => { if (assembled) window.scrollTo({ top: 0, behavior: "auto" }); }, [assembled]);
  async function api(path: string, method = "GET", body?: unknown, credentials = session) {
    const response = await fetch(`/api/practitioner${path}`, {
      method, cache: "no-store", credentials: "same-origin",
      headers: { "Content-Type": "application/json", ...(credentials ? { "X-Review-CSRF": credentials.csrf } : {}) },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "The request could not be accepted. Check the review fields.");
    return result;
  }
  async function act(operation: () => Promise<void>) {
    setBusy(true); setError(""); setMessage("");
    try { await operation(); } catch (e) { setError(e instanceof Error ? e.message : "The review could not be saved."); }
    finally { setBusy(false); }
  }
  useEffect(() => {
    let live = true;
    void fetch("/api/practitioner/session", { cache: "no-store" }).then(async r => {
      if (r.ok && live) setSession(await r.json());
      else if (r.status === 503 && live) setError("Private review is not configured on this machine. Run the local setup described in the practitioner guide.");
    }).catch(() => { if (live) setError("The local review service could not be reached."); });
    return () => { live = false; };
  }, []);
  useEffect(() => {
    if (session) void api("/cases").then(setSavedCases).catch(e => setError(String(e)));
  }, [session, current?.id]);
  useEffect(() => {
    if (!current) return;
    setDraft(parts.map(part => {
      const old = current.claims.find(c => c.question_id === question && c.part === part);
      return old ? editable(old) : { id: null, question_id: question, part, text: "",
        basis: current.demonstration ? "example_content" : "expert_judgment", evidence_ids: [], source_refs: [],
        rationale: "", limitations: "", rejected_alternative: "", practice_kind: part === "practical_application" ? "adaptation" : "not_applicable" };
    }));
    setDirty(false); setChecks({});
  }, [current, question]);
  function patch(index: number, values: Partial<Claim>) {
    setDraft(old => old.map((c, i) => i === index ? { ...c, ...values } : c)); setDirty(true);
  }
  function changeQuestion(next: string) {
    if (!dirty || window.confirm("Discard unsaved changes to this question?")) setQuestion(next);
  }
  const approvedQuestions = current ? Object.keys(current.questions).filter(q =>
    parts.every(p => current.claims.some(c => c.question_id === q && c.part === p && c.status === "approved"))).length : 0;
  const questionEntries = current ? questionOrder.filter(key => key in current.questions).map(key => [key, current.questions[key]]) : [];
  const alert = <>{error && <p className="review-error" role="alert">{error}</p>}{message && <p className="review-message" role="status">{message}</p>}</>;
  if (assembled) return <div className="nadia-report-app">
    <nav className="nadia-report-toolbar"><button onClick={() => setAssembled(null)}>Back to review</button><span>{assembled.demonstration ? "Review-only demonstration" : "Individually reviewed profile"}</span>
      <div className="nadia-report-export"><button onClick={() => saveFile("nadia-individually-reviewed.json", assembled)}>Download reviewed report JSON</button><button onClick={() => window.print()}>Print / save PDF</button></div></nav>
    <ReportContents packet={assembled.packet} individualReview={assembled} />
    <p className="nadia-report-privacy">This report contains private birth data. Review applies only to the displayed individual sections. Automatic personal interpretation remains unapproved.</p>
  </div>;
  return <div className="review-workspace">
    <header className="review-header"><button onClick={onClose}>Back to chart profile</button><span className="review-brand">NADIA / Practitioner</span>
      {session && <div><span>{session.actor}</span><button onClick={() => void act(async () => {
        await api("/logout", "POST"); setSession(null); setCurrent(null); setDraft([]); setHistory(null); setReferences(null); setSavedCases([]);
      })}>Sign out</button></div>}</header>
    {!session ? <main className="review-login"><h1>A private place to make the chart personal.</h1><p>Sign in to inspect evidence, write an interpretation and review each item before it enters a report.</p>
      <form onSubmit={e => { e.preventDefault(); void act(async () => { const result = await api("/login", "POST", { password }, null); setSession(result); setPassword(""); }); }}>
        <label>Practitioner password<input type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} required maxLength={256} /></label>
        <button className="review-primary" disabled={busy}>Sign in</button></form>{alert}
      <p className="review-muted">Local-only access. Cases are stored on this computer, not in your browser or a cloud service. Close this view when you finish.</p>
    </main> : <>
      <section className="review-casebar"><div><h1>{current ? current.packet.profile.name : "Prepare a personal profile"}</h1><p>{current ? `${approvedQuestions} of ${Object.keys(current.questions).length} questions ready · revision ${current.revision}` : "Start with the selected chart, or reopen an existing private case."}</p></div>
        <div className="review-case-actions"><label><input type="checkbox" checked={demo} onChange={e => setDemo(e.target.checked)} />Labeled workflow demonstration</label>
          <button disabled={busy || dirty} onClick={() => void act(async () => { setCurrent(await api("/cases", "POST", { birth, synthetic, demonstration: demo })); setMessage("Case prepared from the existing calculator and source components."); })}>Prepare selected chart</button>
          {savedCases.length > 0 && <label>Reopen case<select value={current?.id ?? ""} onChange={e => e.target.value && void act(async () => { setCurrent(await api(`/cases/${e.target.value}`)); })}><option value="">Choose a saved case</option>{savedCases.map(c => <option value={c.id} key={c.id}>{c.name}{c.demonstration ? " (demonstration)" : ""} / revision {c.revision} / {c.id.slice(0, 6)}</option>)}</select></label>}
        </div></section>
      <div className="review-alerts">{alert}</div>
      {current && <>
        {current.demonstration && <p className="review-demo">Workflow demonstration. Content entered here is example material, not an independently approved expert reading. Exports retain this label.</p>}
        <div className="review-layout">
          <nav className="review-questions" aria-label="Profile questions"><h2>Personal questions</h2><label className="review-mobile-question">Choose a question<select aria-label="Choose a profile question" value={question} onChange={e => changeQuestion(e.target.value)}>{questionEntries.map(([key, title]) => <option value={key} key={key}>{title}</option>)}</select></label>{questionEntries.map(([key, title]) => <button aria-current={question === key ? "step" : undefined} key={key} onClick={() => changeQuestion(key)}>{title}<span>{parts.every(p => current.claims.some(c => c.question_id === key && c.part === p && c.status === "approved")) ? "Ready" : "Incomplete"}</span></button>)}</nav>
          <main className="review-editor"><h2>{current.questions[question]}</h2><p>Write only what you can justify. Each item needs its own evidence, reasoning and limits. A citation alone does not establish that a conclusion follows.</p>
            {draft.map((c, i) => {
              const saved = current.claims.find(s => s.id === c.id);
              return <section className="review-claim" key={c.part} aria-label={partLabel[c.part]}>
                <div className="review-claim-heading"><h3>{partLabel[c.part]}</h3><span className={`review-state state-${saved?.status ?? "draft"}`}>{dirty ? "Unsaved" : saved?.status ?? "Draft"}</span></div>
                <label>Reader-facing text<textarea rows={4} maxLength={4000} value={c.text} onChange={e => patch(i, { text: e.target.value })} /></label>
                <label>Authority classification<select aria-label="Authority classification" value={c.basis} onChange={e => patch(i, { basis: e.target.value as Claim["basis"] })}>
                  {current.demonstration && <option value="example_content">Example content — demonstration only</option>}
                  <option value="expert_judgment">Practitioner judgment — individual case only</option><option value="source_supported">Source-supported interpretation — requires practitioner applicability review</option>
                </select></label>
                <details className="review-claim-evidence"><summary>Evidence and reasoning{c.evidence_ids.length ? ` (${c.evidence_ids.length} linked items)` : " — required before approval"}</summary>
                  <label>Supporting evidence<select aria-label="Supporting evidence" multiple size={5} value={c.evidence_ids} onChange={e => patch(i, { evidence_ids: Array.from(e.target.selectedOptions, o => o.value) })}>{Object.entries(current.preparation.evidence).map(([id, f]) => <option value={id} key={id}>{f.label} ({f.kind})</option>)}</select></label>
                  <label>Source references<select aria-label="Source references" multiple size={5} value={c.source_refs} onChange={e => patch(i, { source_refs: Array.from(e.target.selectedOptions, o => o.value) })}>{current.preparation.source_refs.map(r => <option key={r} value={r}>{r.replace("original-page-", "Original printed page ")}</option>)}</select></label>
                  <label>Why the interpretation follows<textarea rows={3} value={c.rationale} maxLength={4000} onChange={e => patch(i, { rationale: e.target.value })} /></label>
                  <label>Unknown conditions and limits<textarea rows={2} value={c.limitations} maxLength={2000} onChange={e => patch(i, { limitations: e.target.value })} /></label>
                  <label>Rejected alternative<textarea rows={2} value={c.rejected_alternative} maxLength={2000} onChange={e => patch(i, { rejected_alternative: e.target.value })} /></label>
                  {c.part === "practical_application" && <label>Practice provenance<select value={c.practice_kind} onChange={e => patch(i, { practice_kind: e.target.value as Claim["practice_kind"] })}><option value="adaptation">New adaptation</option><option value="source_practice">Sourced practice — applicability must be reviewed</option><option value="not_applicable">Not yet established</option></select></label>}
                </details>
                {saved?.review && <p className="review-muted">Last review by {saved.review.actor}: {saved.review.note}</p>}
                <details className="review-decision"><summary>Review this item</summary>
                  <label>Review note<input value={notes[c.part] ?? ""} maxLength={2000} onChange={e => setNotes({ ...notes, [c.part]: e.target.value })} /></label>
                  <label className="review-check"><input type="checkbox" checked={checks[c.part] ?? false} onChange={e => setChecks({ ...checks, [c.part]: e.target.checked })} />I checked every assertion against this chart, the cited evidence and the unresolved conditions.</label>
                  <div className="review-decisions">{(["approved", "revise", "rejected"] as const).map(decision => <button key={decision} disabled={busy || dirty || !c.id} onClick={() => void act(async () => {
                    setCurrent(await api(`/cases/${current.id}/decision`, "POST", { expected_revision: current.revision, claim_id: c.id, decision, note: notes[c.part] ?? "", assertions_checked: checks[c.part] ?? false, conditions_reviewed: checks[c.part] ?? false }));
                    setMessage(decision === "approved" ? "Item approved for this individual case. No source rule or automated permission changed." : "Review decision saved.");
                  })}>{decision === "approved" ? "Approve individually" : decision === "revise" ? "Request revision" : "Reject"}</button>)}</div>
                </details>
              </section>;
            })}
            <div className="review-save"><button className="review-primary" disabled={!dirty || busy} onClick={() => void act(async () => {
              const other = current.claims.filter(c => c.question_id !== question).map(editable);
              setCurrent(await api(`/cases/${current.id}/claims`, "PUT", { expected_revision: current.revision, claims: [...other, ...draft.map(editable)] })); setMessage("Draft saved. Changed items require a new review.");
            })}>Save question draft</button><p>Edits withdraw approval for the changed item. Nothing is published.</p></div>
          </main>
          <aside className="review-evidence"><h2>Evidence for this chart</h2><p>{current.preparation.selection}</p>
            <details open><summary>Bounded starting points</summary>{current.preparation.bounded_suggestions.map((s, i) => <div key={i}><p>{s.theme ?? "No bounded theme available in the existing finite scope."}</p><p className="review-muted">Suggestion only; complete related-condition interpretation is unresolved.</p></div>)}</details>
            <details><summary>Calculated facts and source components</summary>{Object.entries(current.preparation.evidence).map(([id, f]) => <details key={id}><summary>{f.label}</summary><EvidencePreview value={f.value} /><details><summary>Full protected evidence record</summary><pre>{JSON.stringify(f.value, null, 2)}</pre></details></details>)}</details>
            <details><summary>Rulers, Delegates and represented occupants</summary><pre>{JSON.stringify(current.preparation.relationships, null, 2)}</pre></details>
            <details><summary>Original source evidence</summary><p>Images open only from the authenticated local archive. Missing images remain unavailable.</p>{current.preparation.source_refs.map(ref => <a key={ref} href={`/api/practitioner/source/${encodeURIComponent(ref)}`} target="_blank" rel="noreferrer">{ref.replace("original-page-", "Printed page ")}</a>)}</details>
            <details><summary>Unresolved dependencies</summary><ul>{current.preparation.missing.map(m => <li key={m}>{m}</li>)}</ul></details>
            <details><summary>Expert-reference reconstruction</summary><button onClick={() => void act(async () => setReferences(await api("/references")))}>Load local reference</button>{references?.strongest_reference && <div className="review-reference"><h3>{references.strongest_reference.question}</h3><p>Author conclusion, paraphrased from the cited original example:</p><p>{references.strongest_reference.final_expert_conclusion.text}</p><p className="review-muted">Bounded author-example benchmark. The reconstruction is analyst-authored, not an independently certified universal rule.</p>{references.strongest_reference.intermediate_states.map(s => <p key={s.id}><strong>{s.id.replaceAll("_", " ")}: </strong>{s.meaning}</p>)}<h4>Unexplained transitions and limits</h4><ul>{references.strongest_reference.missing_reasoning.map(m => <li key={m}>{m}</li>)}</ul>{references.source_media?.filter(s => /^original-page-54[0-3]$/.test(s.id)).map(s => <a key={s.id} href={`/api/practitioner/source/${s.id}`} target="_blank" rel="noreferrer">{s.id.replace("original-page-", "Original printed page ")}</a>)}<details><summary>Full typed derivation</summary><pre>{JSON.stringify(references, null, 2)}</pre></details></div>}{references !== null && !references.strongest_reference && <p>No reconstructed reference is installed locally.</p>}</details>
            <details><summary>Review history</summary><button onClick={() => void act(async () => setHistory(await api(`/cases/${current.id}/history`)))}>Load review history</button>{history !== null && <pre>{JSON.stringify(history, null, 2)}</pre>}</details>
            <p className="review-boundary">Calculation verification, source authority, individual review and automated interpretation are separate. Approval here never changes the Knowledge Core.</p>
          </aside>
        </div>
        <section className="review-export"><div><h2>Assemble the reviewed profile</h2><p>Only questions with all three items approved will appear. Incomplete questions stay listed as incomplete.</p></div>
          <button className="review-primary" disabled={!approvedQuestions || busy || dirty} onClick={() => void act(async () => setAssembled(await api(`/cases/${current.id}/report`)))}>Open reviewed report</button>
          <button disabled={busy || dirty} onClick={() => saveFile("nadia-private-review-case.json", current)}>Download private evidence record</button>
        </section>
        <details className="review-secondary-use"><summary>Optional reader feedback</summary><p>Keep voluntary reported experience separate from source fidelity. Agreement does not validate the methodology, and disagreement must be retained.</p>
          <label>Reported by<select aria-label="Feedback reported by" value={feedbackRole} onChange={e => setFeedbackRole(e.target.value)}><option value="reader">The reader</option><option value="third_party">A third party — not the reader’s own assessment</option></select></label>
          <label>Reader feedback<textarea rows={3} maxLength={2000} value={feedback} onChange={e => setFeedback(e.target.value)} /></label>
          <label className="review-check"><input type="checkbox" checked={voluntary} onChange={e => setVoluntary(e.target.checked)} />This feedback was voluntarily supplied for this individual review.</label>
          <button disabled={busy || dirty || !voluntary || feedback.trim().length < 10} onClick={() => void act(async () => { setCurrent(await api(`/cases/${current.id}/feedback`, "POST", { expected_revision: current.revision, text: feedback, reported_by: feedbackRole, voluntarily_supplied: voluntary })); setFeedback(""); setVoluntary(false); setMessage("Reported feedback saved separately. No source or predictive validity was inferred."); })}>Save voluntary feedback</button>
        </details>
        <details className="review-secondary-use"><summary>Separate permission for a future benchmark</summary><p>Default: no secondary use. Record the person’s explicit authorization before including this reading as a private benchmark candidate. A candidate still requires independent review; it is not a gold standard. Demonstration content is excluded.</p>
          <label>Authorization record<textarea value={consent} onChange={e => setConsent(e.target.value)} rows={3} maxLength={2000} /></label>
          <button disabled={current.demonstration || !approvedQuestions || dirty || busy || consent.length < 30} onClick={() => void act(async () => { setCurrent(await api(`/cases/${current.id}/benchmark-consent`, "POST", { expected_revision: current.revision, authorization_record: consent, purpose: "private_benchmark_candidate_only" })); setMessage("Authorization recorded for a candidate only. Independent benchmark review remains required."); })}>Record explicit secondary-use authorization</button>
        </details>
      </>}
      <footer className="review-footer">Private local workspace. Drafts, revisions and review history are stored on this computer. No external inference or analytics is used.</footer>
    </>}
  </div>;
}
