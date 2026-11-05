import React from "react";
import { describe, it, expect, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { acceptProfilePacket, ReportContents, safeBookingUrl, type ProfilePacket } from "./ProfileReport";
import type { Chart } from "./types";
import before from "./__fixtures__/wheel-before.json";
vi.mock("./Wheel", () => ({ Wheel: () => <svg aria-label="Calculated chart" /> }));

const packet: ProfilePacket = {
  schema_version: "nadia-profile/1", report_id: "synthetic-profile-fixture", tier: "essential", synthetic: true,
  profile: { name: "Synthetic profile", birth_date: "1992-07-17", birth_time: "20:01:00", location: "Illustrative Los Alamitos", timezone: "America/Los_Angeles", time_accuracy: "nearest_minute" },
  chart: before.chart as unknown as Chart,
  readiness: { technical_report_ready: true, complete_personal_reading: false, interpretation_status: "blocked", knowledge_status: "verified", limitations: ["Complete contextual synthesis remains unavailable."] },
  sections: [
    { id: "chart-facts", title: "Calculated placements", status: "calculated", summary: "Positions are calculated facts.", facts: [{ label: "Sun", value: "Cancer, house7" }], source_refs: [], rule_ids: [], blockers: [] },
    { id: "vocabulary", title: "Planetary vocabulary", status: "source_vocabulary", summary: "A source-defined function is vocabulary, not a personal conclusion.", facts: [], source_refs: ["original-page-110"], rule_ids: ["internal-rule-not-for-display"], blockers: ["Unfinished synthesis"] },
    { id: "personal", title: "Comprehensive personal interpretation", status: "unavailable", summary: "Additional verified methods are required.", facts: [], source_refs: [], rule_ids: [], blockers: ["Complete contextual synthesis"] },
  ],
  lead: { question: "What is the ONE thing you need to feel loved that other people keep missing?", reflection_question: "When have you felt understood?", personalized_answer: null, booking_url: null },
  core_identity: { version: "0.7.0", commit: "test" },
};

describe("source-governed profile presentation", () => {
  it("separates calculated facts, source vocabulary and unavailable personal interpretation", () => {
    const html = renderToStaticMarkup(<ReportContents packet={packet} />);
    expect(html).toContain("Calculated facts");
    expect(html).toContain("Source vocabulary");
    expect(html).toContain("Interpretation unavailable");
    expect(html).toContain("Original printed page 110");
    expect(html).toContain("Synthetic demonstration");
    expect(html).toContain("Complete personal interpretation is not yet available");
    expect(html).toContain("What is the ONE thing you need to feel loved that other people keep missing?");
    expect(html).toContain("This profile does not yet have a verified personalized answer");
    expect(html).not.toContain("internal-rule-not-for-display");
  });

  it("preserves unknown time and premium limits instead of adding filler", () => {
    const html = renderToStaticMarkup(<ReportContents packet={{ ...packet, tier: "premium", profile: { ...packet.profile, birth_time: null } }} />);
    expect(html).toContain("Unknown — time-dependent results withheld");
    expect(html).toContain("same approved interpretation scope as Essential");
    const partial = { ...packet, readiness: { ...packet.readiness, technical_report_ready: false } };
    expect(acceptProfilePacket(partial)).toBe(partial);
    expect(renderToStaticMarkup(<ReportContents packet={partial} />)).toContain("Some required chart positions are unavailable");
  });

  it("shows a booking invitation only for a configured secure URL", () => {
    const base = renderToStaticMarkup(<ReportContents packet={packet} />);
    expect(base).toContain("A booking destination has not been connected yet");
    expect(base).not.toContain("Explore a full consultation");
    const configured = renderToStaticMarkup(<ReportContents packet={{ ...packet, lead: { ...packet.lead, booking_url: "https://example.org/booking" } }} />);
    expect(configured).toContain('href="https://example.org/booking"');
    expect(configured).toContain('rel="noopener noreferrer"');
    for (const unsafe of ["javascript:alert(1)", "http://example.org/booking", "https://user:secret@example.org/booking", "/invented-booking"]) {
      expect(safeBookingUrl(unsafe)).toBeNull();
    }
  });

  it("rejects any payload promoting full interpretation or a fabricated personalized lead answer", () => {
    expect(acceptProfilePacket(packet)).toBe(packet);
    for (const change of [
      { ...packet, readiness: { ...packet.readiness, complete_personal_reading: true } },
      { ...packet, readiness: { ...packet.readiness, interpretation_status: "approved" } },
      { ...packet, lead: { ...packet.lead, personalized_answer: "You need praise." } },
      { ...packet, sections: [{ ...packet.sections[0], status: "personalized" }] },
    ]) {
      expect(() => acceptProfilePacket(change)).toThrow("interpretation checks");
    }
  });

  it("escapes user names and does not persist or transmit reflection notes", () => {
    const html = renderToStaticMarkup(<ReportContents packet={{ ...packet, profile: { ...packet.profile, name: '<script>alert("name")</script>' } }} />);
    expect(html).not.toContain('<script>alert("name")</script>');
    expect(html).toContain("&lt;script&gt;");
    expect(html).toContain("not sent, saved or included in the report export");
    expect(html).toMatch(/maxlength="2000"/i);
  });
});
