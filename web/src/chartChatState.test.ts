import { describe, expect, it } from "vitest";
import { chatIdentity, isChatReply, readChatState, recentChatHistory, type ChatExchange, type ChatReply } from "./chartChatState";
import type { BirthInput } from "./types";

const input: BirthInput = { name: "Fictional chart", local_date: "2000-01-01", local_time: "12:00:00", timezone: "UTC", fold: null, latitude: 0, longitude: 0, location_name: "Test", coordinate_provenance: "User entered", time_accuracy: "nearest_minute", uncertainty_seconds: 30, objects: ["Sun"], chart_type: "natal" };
const reply: ChatReply = { schema_version: "chart-chat-reply-v1", reply_id: "reply", chart_id: "chart", question: "What stands out?", answer: "A supported reflection.", follow_up: "What feels relevant?", provider: "OpenRouter", model: "deepseek/deepseek-v4.1-flash-1017", personal_report_approved: false,
  evidence: { context_sha256: "hash", phddasr_order: ["planet", "house"], facts: {}, assessments: {}, current_sky: null, sources: [], context_source_ids: [], source_fingerprint: {}, complete_phddasr: false } };
const exchange: ChatExchange = { id: "turn", question: reply.question, reply, created_at: "2026-10-28T12:00:00Z" };

describe("chart conversation isolation and recovery", () => {
  it("keeps a conversation when only object visibility or wheel type changes", () => {
    expect(chatIdentity(input)).toBe(chatIdentity({ ...input, objects: ["Sun", "Moon"], chart_type: "dual" }));
  });
  it("separates another person, birth time and DST occurrence", () => {
    for (const changed of [{ name: "Other person" }, { local_time: "13:00:00" }, { fold: 1 as const }, { latitude: 1 }])
      expect(chatIdentity(input)).not.toBe(chatIdentity({ ...input, ...changed }));
  });
  it("restores exact questions and replies only to their matching chart", () => {
    const identity = chatIdentity(input);
    const raw = JSON.stringify({ schema_version: "chart-chat-local-v1", chart_signature: identity, draft: "Next question", exchanges: [exchange] });
    expect(readChatState(raw, identity).exchanges).toEqual([exchange]);
    expect(readChatState(raw, chatIdentity({ ...input, name: "Other" })).exchanges).toEqual([]);
  });
  it("rejects corrupted or mismatched stored conversation data", () => {
    const id = chatIdentity(input);
    for (const raw of ["bad json", "null", JSON.stringify({ schema_version: "old" }), JSON.stringify({ schema_version: "chart-chat-local-v1", chart_signature: id, draft: "", exchanges: [{ ...exchange, question: "A different question" }] })])
      expect(readChatState(raw, id).exchanges).toEqual([]);
  });
  it("rejects malformed evidence rather than crashing its renderer", () => {
    expect(isChatReply(reply)).toBe(true);
    expect(isChatReply({ ...reply, evidence: { ...reply.evidence, assessments: { Sun: { stages: "bad" } } } })).toBe(false);
    expect(isChatReply({ ...reply, evidence: { ...reply.evidence, current_sky: { as_of_utc: "now", sky_to_natal_geometry: [["Sun", "Moon", null]] } } })).toBe(false);
  });
  it("sends only user/assistant text history, keeping full local records intact", () => {
    const turns = Array.from({ length: 15 }, (_, i) => ({ ...exchange, id: String(i), question: `Question ${i}` }));
    const history = recentChatHistory(turns);
    expect(history).toHaveLength(20);
    expect(history[0]).toEqual({ role: "user", content: "Question 5" });
    expect(history.every((v) => ["user", "assistant"].includes(v.role))).toBe(true);
    expect(JSON.stringify(history)).not.toContain("source_fingerprint");
    expect(turns).toHaveLength(15);
  });
});
