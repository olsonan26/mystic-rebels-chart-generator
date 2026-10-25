import React from "react";
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { GradityDetails, MethodVerification } from "./MethodVerification";

describe("scoped method evidence presentation", () => {
  it("shows exact source status and contradiction instead of implying general scientific validation", () => {
    const markup = renderToStaticMarkup(<MethodVerification rules={{
      gradity: { status: "VERIFIED", evidence: "PDF 203 / reflow 207 / original 143; PDF 477 / original 569", verification_scope: "documented method and sampled astronomy", id: "gradity-v1" },
      spark: { status: "BLOCKED", reason: "House and sign parity conflict." },
    }} />);
    expect(markup).toContain("<summary>Method verification</summary>");
    expect(markup).toContain("Verified method");
    expect(markup).toContain("PDF 203 / reflow 207 / original 143");
    expect(markup).toContain("House and sign parity conflict.");
    expect(markup).toContain("does not establish scientific evidence for an interpretation");
    expect(markup).not.toContain("<details open");
  });
  it("preserves raw event fields and keeps a null phase visible as an unassigned boundary", () => {
    const point = { group: "Planets", retrograde: false, gradity: { phase: null, status: "BOUNDARY" as const, reason: "Exact equality is unassigned.", events: [{ kind: "station_direct", utc: "2024-04-25T12:54:00Z", longitude_deg: 15.968123456789, root_bracket_tolerance_seconds: 0.01 }], source: { pdf_pages: [203,477], original_printed_pages: [143,569], reflow_pages: [207,481] } } };
    const markup = renderToStaticMarkup(<GradityDetails point={point} />);
    expect(markup).toContain("Exact equality is unassigned.");
    expect(markup).toContain("15.968123456789");
    expect(markup).toContain("root_bracket_tolerance_seconds");
    expect(markup).toContain("PDF page 203, 477; original printed page 143, 569; reflow page 207, 481");
    expect(markup).not.toContain("Pregrade");
    expect(renderToStaticMarkup(<GradityDetails point={{ ...point, gradity: { phase: null, status: "NOT_APPLICABLE", reason: "Mathematical point." } }} />)).toBe("");
  });
});
