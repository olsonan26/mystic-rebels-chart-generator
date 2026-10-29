import type { BirthInput } from "./types";

export type ChatFact = {
  id: string;
  layer: "natal" | "sky";
  display_dms: string;
  house: number | null;
  sign_ruler: string;
  pulse: string;
  retrograde: boolean | null;
  natal_overlay_house?: number | null;
  as_of_utc?: string;
};
export type ChatEvidence = {
  context_sha256: string;
  phddasr_order: string[];
  facts: Record<string, ChatFact>;
  assessments: Record<string, {
    stages: { stage: string; status: string; [key: string]: unknown }[];
    ruler_route: { path: string[]; repeat: string | null };
  }>;
  current_sky: null | {
    as_of_utc: string;
    sky_to_natal_geometry: [string, string, number, number, number][];
    timing_limit: string;
  };
  sources: {
    concept_id: string;
    title: string;
    source_meaning: string;
    exceptions: string[];
    citations: { original_printed_pages?: string[]; pdf_page?: number; file_id?: string }[];
  }[];
  context_source_ids: string[];
  source_fingerprint: Record<string, unknown>;
  complete_phddasr: false;
  [key: string]: unknown;
};
export type ChatReply = {
  schema_version: "chart-chat-reply-v1";
  reply_id: string;
  chart_id: string;
  question: string;
  answer: string;
  follow_up: string;
  provider: string;
  model: string;
  evidence: ChatEvidence;
  personal_report_approved: false;
};
export type ChatExchange = { id: string; question: string; reply: ChatReply; created_at: string };
export type ChatState = { schema_version: "chart-chat-local-v1"; chart_signature: string; draft: string; exchanges: ChatExchange[] };

/** Object visibility and wheel design do not change the person's conversation. */
export function chatIdentity(input: BirthInput): string {
  const { objects: _objects, chart_type: _type, ...birth } = input;
  return JSON.stringify(Object.fromEntries(Object.entries(birth).sort(([a], [b]) => a.localeCompare(b))));
}
export function chatStorageKey(identity: string): string {
  return "mystic-rebels:chart-chat:v1:" + identity;
}
export function isChatReply(value: unknown): value is ChatReply {
  if (!value || typeof value !== "object") return false;
  const r = value as Partial<ChatReply>;
  return r.schema_version === "chart-chat-reply-v1" && typeof r.reply_id === "string" &&
    typeof r.chart_id === "string" && typeof r.question === "string" &&
    typeof r.answer === "string" && r.answer.length > 0 && r.answer.length <= 24000 &&
    typeof r.follow_up === "string" && !!r.evidence &&
    typeof r.evidence.facts === "object" && r.evidence.facts !== null &&
    typeof r.evidence.assessments === "object" && r.evidence.assessments !== null &&
    Array.isArray(r.evidence.sources) && r.evidence.sources.every((s) => s && typeof s.title === "string" && typeof s.concept_id === "string" && Array.isArray(s.citations)) &&
    Array.isArray(r.evidence.phddasr_order) && r.evidence.phddasr_order.every((s) => typeof s === "string") &&
    Object.values(r.evidence.assessments).every((a) => a && Array.isArray(a.stages) &&
      a.stages.every((s) => s && typeof s.stage === "string" && typeof s.status === "string") &&
      a.ruler_route && Array.isArray(a.ruler_route.path)) &&
    (r.evidence.current_sky === null || (!!r.evidence.current_sky && typeof r.evidence.current_sky.as_of_utc === "string" &&
      Array.isArray(r.evidence.current_sky.sky_to_natal_geometry) && r.evidence.current_sky.sky_to_natal_geometry.every((g) =>
        Array.isArray(g) && g.length === 5 && typeof g[0] === "string" && typeof g[1] === "string" && g.slice(2).every((n) => typeof n === "number" && Number.isFinite(n))))) &&
    Array.isArray(r.evidence.context_source_ids);
}
export function readChatState(raw: string | null, identity: string): ChatState {
  const empty: ChatState = { schema_version: "chart-chat-local-v1", chart_signature: identity, draft: "", exchanges: [] };
  try {
    if (!raw) return empty;
    const data = JSON.parse(raw) as ChatState;
    if (data.schema_version !== empty.schema_version || data.chart_signature !== identity ||
      typeof data.draft !== "string" || data.draft.length > 4000 || !Array.isArray(data.exchanges) ||
      !data.exchanges.every((t) => typeof t.id === "string" && typeof t.created_at === "string" &&
        typeof t.question === "string" && t.question.length <= 4000 && isChatReply(t.reply) && t.reply.question === t.question)) return empty;
    return data;
  } catch { return empty; }
}
export function recentChatHistory(exchanges: ChatExchange[]): { role: "user" | "assistant"; content: string }[] {
  return exchanges.flatMap((turn) => [
    { role: "user" as const, content: turn.question },
    { role: "assistant" as const, content: (turn.reply.answer + (turn.reply.follow_up ? "\n\n" + turn.reply.follow_up : "")).slice(0, 6000) },
  ]).slice(-20);
}
