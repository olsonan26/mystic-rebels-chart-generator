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
  condition_graph?: {
    catalog_inventory_complete: boolean;
    evaluated_catalog_ids: string[];
    unavailable: { id: string }[];
    nodes: Record<string, {
      fact_ref: string;
      physical_retrograde: boolean | null;
      sign_ruler_ref: string | null;
      house_delegate_ref: string | null;
      house_delegate_retrograde: boolean | null;
      ruled_areas: { sign: string; house: number | null; occupant_condition_refs: string[] }[];
      missing_dependencies: string[];
      full_condition_complete: false;
    }>;
    direct_conjunction_reach: { id: string; sender: string; receiver: string; separation_deg: number; radius_deg: number; interpretive_roles_assigned: false }[];
  };
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
function isConditionGraph(value: unknown): boolean {
  if (!value || typeof value !== "object") return false;
  const g = value as NonNullable<ChatEvidence["condition_graph"]>;
  const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every((s) => typeof s === "string");
  const nullableString = (v: unknown) => v === null || typeof v === "string";
  const nullableBoolean = (v: unknown) => v === null || typeof v === "boolean";
  return typeof g.catalog_inventory_complete === "boolean" && strings(g.evaluated_catalog_ids) &&
    Array.isArray(g.unavailable) && g.unavailable.every((v) => v && typeof v.id === "string") &&
    !!g.nodes && typeof g.nodes === "object" && Object.values(g.nodes).every((n) => n &&
      typeof n.fact_ref === "string" && nullableString(n.sign_ruler_ref) && nullableString(n.house_delegate_ref) &&
      nullableBoolean(n.physical_retrograde) && nullableBoolean(n.house_delegate_retrograde) && n.full_condition_complete === false &&
      strings(n.missing_dependencies) && Array.isArray(n.ruled_areas) && n.ruled_areas.every((a) => a &&
        typeof a.sign === "string" && (a.house === null || (Number.isInteger(a.house) && a.house >= 1 && a.house <= 12)) && strings(a.occupant_condition_refs))) &&
    Array.isArray(g.direct_conjunction_reach) && g.direct_conjunction_reach.every((c) => c &&
      typeof c.id === "string" && typeof c.sender === "string" && typeof c.receiver === "string" &&
      Number.isFinite(c.separation_deg) && Number.isFinite(c.radius_deg) && c.interpretive_roles_assigned === false);
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
    (r.evidence.condition_graph === undefined || isConditionGraph(r.evidence.condition_graph)) &&
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
