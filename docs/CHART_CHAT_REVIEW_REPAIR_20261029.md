# Suggested-question verification failure — 29 October 2026

The owner reported the red message “I could not verify a grounded answer to that wording” after selecting the built-in **What patterns stand out in my chart?** suggestion, with current sky enabled. That message maps specifically to `CHAT_UNVERIFIED`, after the writer/reviewer calls, rather than connection, balance or timeout errors. The screenshot does not expose the original chart or raw production response, so the precise original production rejection cannot be reconstructed from it alone.

## Reproduction and cause

The same question and current-sky option reproduced the identical error locally using the documented illustrative chart under a fictional QA name and the existing authorized OpenRouter model. The first draft passed structural checks. The second response contained `claims` and `follow_up`, but omitted the required boolean `approved`. Pydantic rejected it with `approved: Field required`. The server then returned the screenshot's generic error. Fictional model diagnostics stay in ignored `tmp/`, not the public repository.

The reviewer prompt reused the complete writer prompt, including **Return JSON with exactly claims and follow_up** and a writer-only JSON example. An appended reviewer instruction requested `approved`, creating a contradictory response contract. This is an application integration defect; the suggested question is valid. No evidence establishes a Supabase outage or lost chart data.

Ranked diagnostic possibilities were: missing/malformed review schema, invalid source/fact/stage references, or an explicit semantic rejection (`approved=false`). Inspecting the captured fictional draft/review distinguished them: the reproduced failure was the missing approval field, not an explicit rejection or invalid first-draft references.

## Fix

- Give the reviewer a dedicated, consistent response contract and example containing **claims, follow_up and required boolean approved**. Preserve the shared source and method limits.
- Allow at most one repair pass for a malformed or structurally invalid review, supplying the exact validation issues and unchanged evidence. The existing 48-second total deadline includes this pass. A failed repair remains blocked; approval is never assumed or defaulted. An explicit `approved=false` receives no retry.
- Replace the “try a more specific question” message with a truthful answer-verification failure notice that keeps the question. The application must not blame a valid suggested question for a model-formatting failure.
- Log only fixed rejection categories and attempt counts, not question text, birth details, model prose, provider error bodies or credentials. Preserve separate optional repair usage metadata.

## Verification

Two regression tests failed against the previous implementation: recovery from a missing approval field and failure after an unsuccessful bounded repair. They passed after the fix. The focused chatbot, chart API and access suite passed **117 tests**, including secret/private-text logging checks and continued rejection of forged citations, unsupported mechanisms, extra approval overrides and explicit review refusals.

The exact previously failing question then returned a structurally checked, explicitly approved real OpenRouter answer for the same fictional QA chart. This is local provider verification, not an authenticated production execution test or empirical validation of the reading. The owner's previous request to skip authenticated production testing remains in effect. The patch is a separate release from the 28 October deployment; its deployment status must be established explicitly rather than inferred from Git publication.
