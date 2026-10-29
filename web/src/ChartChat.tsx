import { memo, useEffect, useRef, useState } from "react";
import { ArrowDownToLine, ArrowUp, ChevronDown, LoaderCircle, MessageCircle, X } from "lucide-react";
import type { Chart } from "./types";
import {
  chatIdentity, chatStorageKey, isChatReply, readChatState, recentChatHistory,
  type ChatEvidence, type ChatExchange,
} from "./chartChatState";
import "./chartChat.css";

const Evidence = memo(function Evidence({ evidence }: { evidence: ChatEvidence }) {
  const [point, setPoint] = useState("Sun");
  const assessment = evidence.assessments[point];
  const facts = Object.values(evidence.facts).filter((p) => p?.layer === "natal" && evidence.assessments[p.id]);
  const sky = evidence.current_sky;
  const skyPoints = Object.values(evidence.facts).filter((p) => p?.layer === "sky");
  const closest = [...(sky?.sky_to_natal_geometry ?? [])].sort((a, b) => a[4] - b[4]).slice(0, 10);
  return <details className="chart-chat-evidence">
    <summary>Why this answer? <ChevronDown size={14} /></summary>
    <div className="chart-chat-evidence-body">
      <p>The answer uses this chart and reviewed source components. The full degree-meaning and directed-aspect method remains incomplete.</p>
      <label>Explore a chart factor
        <select value={point} onChange={(e) => setPoint(e.target.value)}>
          {facts.map((p) => <option key={p.id} value={p.id}>{p.id} · {p.display_dms}</option>)}
        </select>
      </label>
      {assessment && <>
        <ol className="chart-chat-stages">{assessment.stages.map((s) => <li key={s.stage}>
          <strong>{s.stage[0].toUpperCase() + s.stage.slice(1)}</strong>
          <span>{String(s.status).replaceAll("_", " ")}</span>
          <small>{Object.entries(s).filter(([key, value]) => !["stage", "status", "note", "parent_convention"].includes(key) && value !== null && !Array.isArray(value))
            .map(([key, value]) => `${key.replaceAll("_", " ")}: ${String(value)}`).join("; ")}</small>
        </li>)}</ol>
        <p>Ruler route: {assessment.ruler_route.path.join(" → ")}{assessment.ruler_route.repeat ? ` → ${assessment.ruler_route.repeat} (repeats)` : ""}.</p>
      </>}
      {sky && <>
        <h4>Sky context</h4>
        <p><time dateTime={sky.as_of_utc}>{new Date(sky.as_of_utc).toLocaleString()}</time> · {Intl.DateTimeFormat().resolvedOptions().timeZone}</p>
        <div className="chart-chat-geometry"><table><thead><tr><th>Sky point</th><th>Position</th><th>Natal sector</th></tr></thead>
          <tbody>{skyPoints.map((p) => <tr key={p.id}><td>{p.id}{p.retrograde ? " ℞" : ""}</td><td>{p.display_dms}</td><td>{p.natal_overlay_house ?? "Unknown"}</td></tr>)}</tbody></table></div>
        <p>These are the closest angular matches in this snapshot. They are geometry diagnostics, not qualified aspects or a ranking of influence.</p>
        <div className="chart-chat-geometry"><table><thead><tr><th>Sky → natal</th><th>Separation</th><th>Offset*</th></tr></thead>
          <tbody>{closest.map((r) => <tr key={`${r[0]}:${r[1]}`}><td>{r[0]} → {r[1]}</td><td>{r[2].toFixed(3)}°</td><td>{r[4].toFixed(3)}°</td></tr>)}</tbody></table></div>
        <small>*Offset from the nearest diagnostic angle, not an influence orb. No event peak or duration has been inferred.</small>
      </>}
      {evidence.sources.length > 0 && <><h4>Sources used</h4>{evidence.sources.map((s) => <details key={s.concept_id}>
        <summary>{s.title}</summary><p>{s.source_meaning}</p>
        {s.exceptions?.length > 0 && <ul>{s.exceptions.map((v) => <li key={v}>{v}</li>)}</ul>}
        <small>{s.concept_id} · {Array.from(new Set(s.citations?.flatMap((c) => c.original_printed_pages ?? (c.pdf_page ? [`PDF ${c.pdf_page}`] : [])))).join(", ")}</small>
      </details>)}</>}
      <p className="chart-chat-fingerprint">The downloaded conversation includes chart facts, source hashes, claim references and this explanation.</p>
    </div>
  </details>;
});

export default function ChartChat({ chart, generation, stale, obscured }: { chart: Chart; generation: number; stale: boolean; obscured: boolean }) {
  const identity = chatIdentity(chart.input);
  const [saved] = useState(() => {
    try { return readChatState(localStorage.getItem(chatStorageKey(identity)), identity); }
    catch { return readChatState(null, identity); }
  });
  const [open, setOpen] = useState(generation > 0);
  const [draft, setDraft] = useState(saved.draft);
  const [exchanges, setExchanges] = useState<ChatExchange[]>(saved.exchanges);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [storageWarning, setStorageWarning] = useState("");
  const [connection, setConnection] = useState<boolean | null>(null);
  const [includeCurrent, setIncludeCurrent] = useState(true);
  const [asOf, setAsOf] = useState("");
  const [showDate, setShowDate] = useState(false);
  const [preview, setPreview] = useState<ChatEvidence | null>(null);
  const input = useRef<HTMLTextAreaElement>(null);
  const launcher = useRef<HTMLButtonElement>(null);
  const bottom = useRef<HTMLDivElement>(null);
  const controller = useRef<AbortController | null>(null);
  const latest = useRef({ draft, exchanges });
  latest.current = { draft, exchanges };

  function close() { setOpen(false); requestAnimationFrame(() => launcher.current?.focus()); }
  useEffect(() => { if (generation > 0) setOpen(true); }, [generation]);
  useEffect(() => {
    if (!open || obscured) return;
    requestAnimationFrame(() => input.current?.focus());
    const onEscape = (e: KeyboardEvent) => { if (e.key === "Escape") close(); };
    window.addEventListener("keydown", onEscape);
    const abort = new AbortController();
    fetch("/api/chart-chat/status", { signal: abort.signal }).then((r) => {
      if (!r.ok) throw new Error("Chat unavailable"); return r.json();
    }).then((v) => setConnection(v.configured === true)).catch((e) => { if (e.name !== "AbortError") setConnection(false); });
    return () => { window.removeEventListener("keydown", onEscape); abort.abort(); };
  }, [open, obscured]);
  useEffect(() => () => controller.current?.abort(), []);
  useEffect(() => {
    const saveLatest = () => {
      try { localStorage.setItem(chatStorageKey(identity), JSON.stringify({ schema_version: "chart-chat-local-v1", chart_signature: identity, ...latest.current })); }
      catch { /* The visible quota warning and export remain the recovery path. */ }
    };
    const onVisibility = () => { if (document.visibilityState === "hidden") saveLatest(); };
    window.addEventListener("pagehide", saveLatest);
    document.addEventListener("visibilitychange", onVisibility);
    return () => {
      window.removeEventListener("pagehide", saveLatest);
      document.removeEventListener("visibilitychange", onVisibility);
      saveLatest();
    };
  }, [identity]);
  useEffect(() => { bottom.current?.scrollIntoView({ block: "nearest", behavior: "auto" }); }, [exchanges.length, busy, error, open]);
  useEffect(() => {
    const timer = setTimeout(() => {
      try {
        localStorage.setItem(chatStorageKey(identity), JSON.stringify({ schema_version: "chart-chat-local-v1", chart_signature: identity, draft, exchanges }));
        setStorageWarning("");
      } catch { setStorageWarning("Your browser could not save this update. Download the chat to keep it."); }
    }, 350);
    return () => clearTimeout(timer);
  }, [draft, exchanges, identity]);

  function download() {
    const packet = { schema_version: "mystic-chart-conversation-v1", chart_id: chart.chart_id,
      birth_input: chart.input, chart_signature: identity, exported_at_utc: new Date().toISOString(),
      exchanges, unanswered_question: draft, current_context_enabled: includeCurrent, selected_context_date_utc: asOf || "now" };
    const url = URL.createObjectURL(new Blob([JSON.stringify(packet, null, 2)], { type: "application/json" }));
    const a = document.createElement("a"); a.href = url;
    a.download = `mystic-rebels-${chart.input.name.replace(/[^a-z0-9]+/gi, "-").slice(0, 50) || "chart"}-chat.json`;
    a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function send(contextOnly = false) {
    const question = draft.trim();
    if (!question || busy || stale) return;
    const requestChart = chart.chart_id;
    const abort = new AbortController(); controller.current = abort;
    setBusy(true); setError("");
    try {
      const response = await fetch(contextOnly ? "/api/chart-chat/context" : "/api/chart-chat", {
        method: "POST", headers: { "Content-Type": "application/json" }, signal: abort.signal,
        body: JSON.stringify({ birth: chart.input, chart_id: requestChart, question,
          history: recentChatHistory(exchanges), include_current: includeCurrent,
          as_of: includeCurrent ? (asOf ? `${asOf}:00Z` : new Date().toISOString()) : null }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error?.message ?? result.detail?.[0]?.msg ?? "Chat could not finish. Your question is kept; try again.");
      if (contextOnly) { setPreview(result as ChatEvidence); return; }
      if (!isChatReply(result) || result.chart_id !== requestChart || result.question !== question)
        throw new Error("The reply did not match this chart. Your question is kept; try again.");
      setExchanges((old) => [...old, { id: crypto.randomUUID(), question, reply: result, created_at: new Date().toISOString() }]);
      setDraft(""); setPreview(null);
    } catch (e) {
      if (!abort.signal.aborted) setError(e instanceof Error ? e.message : "Chat is unavailable. Your question is kept.");
    } finally {
      if (!abort.signal.aborted) { setBusy(false); controller.current = null; }
    }
  }

  return <>
    <button ref={launcher} className="chart-chat-launcher" type="button" disabled={obscured} aria-expanded={open} aria-controls="chart-chat-panel" onClick={() => setOpen((v) => !v)}>
      <MessageCircle size={20} /><span>Ask about your chart</span>
    </button>
    {open && <section id="chart-chat-panel" className="chart-chat-panel" role="dialog" aria-modal="false" aria-hidden={obscured} inert={obscured || undefined} aria-labelledby="chart-chat-heading">
      <header className="chart-chat-header"><div><span className="chart-chat-person">{chart.input.name || "Your chart"}</span>
        <h2 id="chart-chat-heading">What do you want to know?</h2></div>
        <div className="chart-chat-actions"><button type="button" title="Download conversation" aria-label="Download conversation" onClick={download}><ArrowDownToLine size={18} /></button>
          <button type="button" aria-label="Close chart chat" onClick={close}><X size={20} /></button></div>
      </header>
      <div className="chart-chat-conversation" role="log" aria-live="polite" aria-relevant="additions">
        {exchanges.length === 0 && <div className="chart-chat-welcome"><p>Ask about your chart, your relationships, your work, or what you’re navigating now.</p>
          <div className="chart-chat-suggestions">{["What patterns stand out in my chart?", "What can I explore about relationships?", "What is happening in the sky right now?"].map((q) =>
            <button key={q} type="button" onClick={() => { setDraft(q); input.current?.focus(); }}>{q}</button>)}</div></div>}
        {exchanges.map((turn) => <article className="chart-chat-exchange" key={turn.id}>
          <div className="chart-chat-question"><span className="sr-only">You asked: </span>{turn.question}</div>
          <div className="chart-chat-answer"><span className="sr-only">Chart assistant: </span>{turn.reply.answer.split(/\n\s*\n/).map((p, i) => <p key={i}>{p}</p>)}
            {turn.reply.follow_up && <p className="chart-chat-followup">{turn.reply.follow_up}</p>}
            <Evidence evidence={turn.reply.evidence} /></div>
        </article>)}
        {busy && <div className="chart-chat-thinking" role="status"><LoaderCircle size={17} className="chart-chat-spin" /> Reading the chart and checking the evidence…</div>}
        {preview && <Evidence evidence={preview} />}
        {error && <p className="chart-chat-error" role="alert">{error}</p>}
        <div ref={bottom} />
      </div>
      <form className="chart-chat-composer" onSubmit={(e) => { e.preventDefault(); void send(); }}>
        {stale && <p className="chart-chat-notice">Generate the updated chart before asking about edited birth details.</p>}
        {connection === false && <p className="chart-chat-notice">The reading service isn’t connected yet. Your question can stay here while the site owner connects it.</p>}
        {storageWarning && <p className="chart-chat-notice" role="status">{storageWarning}</p>}
        <div className="chart-chat-options"><label><input type="checkbox" checked={includeCurrent} onChange={(e) => setIncludeCurrent(e.target.checked)} /> Include the current sky</label>
          {includeCurrent && <button type="button" onClick={() => setShowDate((v) => !v)}>{asOf ? "Selected date" : "Now"} <ChevronDown size={13} /></button>}</div>
        {showDate && includeCurrent && <label className="chart-chat-date">Sky date and time (UTC)
          <input type="datetime-local" value={asOf} min="1800-01-01T00:00" max="2399-12-31T23:59" onChange={(e) => setAsOf(e.target.value)} />
          <button type="button" onClick={() => { setAsOf(""); setShowDate(false); }}>Use now</button></label>}
        <label className="sr-only" htmlFor="chart-chat-question">Your question</label>
        <div className="chart-chat-input-row"><textarea id="chart-chat-question" ref={input} value={draft} maxLength={4000} rows={3}
          disabled={busy} placeholder="Ask what’s on your mind…" onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); void send(); } }} />
          <button className="chart-chat-send" type="submit" disabled={!draft.trim() || busy || stale || connection !== true} aria-label="Send question"><ArrowUp size={21} /></button></div>
        <div className="chart-chat-foot"><span>Chart readings through OpenRouter</span>
          <button type="button" disabled={!draft.trim() || busy || stale} onClick={() => void send(true)}>See chart context</button></div>
        <small className="chart-chat-data-note">Replies use your chart and recent messages. Download this chat to keep a separate copy.</small>
      </form>
    </section>}
  </>;
}
