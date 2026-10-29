# Chart chat: DeepSeek connection and source-packet contract

Researched 28 October 2026, America/Denver, for the requested chat that opens after chart generation with “What do you want to know?” Provider documentation and local authorities were inspected directly. Initial research preceded credentials. The subsequent implementation uses the owner's selected OpenRouter connection and has made real calls with fictional chart data; credentials are excluded from this document and Git. Canonical full-report approval flags remain unchanged.

## Selected implementation: OpenRouter

The owner selected OpenRouter in response to the explicit chart/question/history-sharing question. Runtime configuration is server-side `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`, default **`deepseek/deepseek-v4.1-flash-1017`**. This exact model ID was verified in the [official live model catalog](https://openrouter.ai/api/v1/models), rather than assuming the model name from the conversational label “DeepSeek 4.1”. Calls use only `https://openrouter.ai/api/v1/chat/completions`, with JSON output, `reasoning: {effort: "none", exclude: true}` and complete final content. [OpenRouter API reference](https://openrouter.ai/docs/api_reference/overview).

The implementation uses `httpx==0.28.1`, streaming transport with non-streaming model output, a bounded response body, per-call timeouts and a combined 48-second deadline for calculation plus writer/reviewer passes. Reasons, raw provider errors and credentials are not returned. The initial direct-provider findings below explain the comparison; they are not the active configuration. See [the implemented feature guide](CHART_CHAT.md) for source gates, actual verification and remaining limits.

## Initial direct-provider comparison

Use server-side `DEEPSEEK_API_KEY` and configurable `DEEPSEEK_MODEL`, defaulting to `deepseek-flash`. The official first-call guide identifies that API name as the current V4.1 Flash deployment. Send JSON over HTTPS to `https://api.deepseek.com/chat/completions` with Bearer authorization. The key must never enter browser configuration, exports or Git. [Official first-call guide](https://api-docs.deepseek.com/).

For a first implementation, request non-streaming output with `thinking: {type: "disabled"}`, bounded `max_tokens`, and `response_format: {type: "json_object"}`. Parse the final `choices[0].message.content`, not `reasoning_content`. Require a complete `finish_reason="stop"`; reject truncated, filtered, tool-call or interrupted responses. Retain the returned model, request ID and numeric usage separately from prose. JSON mode is not a schema or source-support validator. [Chat-completions reference](https://api-docs.deepseek.com/api/create-chat-completion/).

The prompt must explicitly request JSON, include the word `json`, and show the expected object. The provider warns that empty content can occur and token limits can truncate JSON. Reject empty/malformed output rather than displaying it as a successful answer. [JSON-output guide](https://api-docs.deepseek.com/guides/json_mode/).

Thinking is enabled by default, so explicitly disable it for this path. In ordinary chat without tools, prior reasoning content is unnecessary; do not retain or expose it. A reviewer pass should also return only its final structured result. [Thinking-mode guide](https://api-docs.deepseek.com/guides/thinking_mode/).

Map errors into useful application states: 401 key/authentication; 402 balance; 400/422 configuration/request; 429 rate/concurrency; 500/503 transient provider failure. Avoid returning raw provider bodies that may echo sensitive inputs. Keep the failed question available for an explicit retry. [Error-code reference](https://api-docs.deepseek.com/quick_start/error_codes/).

Non-streaming responses may contain leading empty keep-alive lines; parse the complete JSON body with whitespace tolerated. Apply an application deadline rather than inheriting the provider's much longer possible queue wait. Optional `user_id` isolation must use a non-identifying opaque ID, never a name or birth details. [Rate-limit and isolation guide](https://api-docs.deepseek.com/quick_start/rate_limit/).

The local `vercel.json` gives `api/index.py` a 60-second function budget. A writer/reviewer implementation needs explicit combined deadlines below that limit, including chart/context calculation time. Standard-library HTTP is sufficient; a new model SDK is not required. `api/index.py` already wraps the ASGI app in `SitePasswordGate`, so a new router must remain inside that same protected application.

## Canonical source-use boundaries

`knowledge_audit/report_components.py#usage_catalog` and the portable manifest deliberately distinguish:

| Use | Current contract |
|---|---|
| Explain and cite source concepts | Allowed with their actual limitations and competing witnesses |
| Attach eligible reviewed vocabulary to calculated natal facts | Allowed as scoped component annotation |
| Offer a conditional component reflection or practical question | Proposed bounded chat composition, not a new approval inferred from the catalog; keep component evidence/incompleteness explicit and separately review the composition |
| Treat a source keyword as a definite event, biography or guaranteed outcome | Unsupported |
| Resolve contradictory rules or substitute generic-library astrology | Unsupported |
| Mark the full personal-report engine approved | Remains false |

The existing catalog has `personal_trait_claim_allowed=False`, `completed_personal_report_approved=False` and `external_library_fallback_allowed=False`. `NOT_APPROVED` does not prohibit reading the book's reviewed summaries; it does block converting those summaries into unrestricted personal conclusions. Reuse the catalog's actual eligible component flags. Eunomia must retain both cited alternatives without a winner; Chiron must retain its reviewed vocabulary and held-out example/orbit issues.

User-reported circumstances and prior assistant messages are conversation context. They are not chart-derived observations or authority for changing chart facts. Answers may be useful and natural without reproducing internal status labels in every sentence; an explanation view should show the actual source/claim limitations.

## Packet assembly and fingerprint verification

Authority is `data/knowledge/report_knowledge_manifest.json`, then the current canonical files. Do not use only a small hand-selected glossary. The existing export generator already demonstrates dependency closure and preservation of assertions/findings in `scripts/export_report_knowledge.py#build`.

1. Resolve question relevance from explicit roots and a transparent lexical/topic plan. Relevance selection is an engineering choice, not a new planetary strength ranking.
2. Include `objective-context`, `agency`, `phsr`, `planet-lexicon`, `house-field`, `tone-pulse` and appropriate condition/directional/degree context. Include all applicable record `requires_concepts` and assertion `requires_concepts` transitively. Preserve unknown dependency errors.
3. Profile IDs such as `sign-aries` are not inventory record IDs. Resolve their `source_concept_id` (for signs, `tone-pulse`) and profile `dependencies`; retain profile exceptions, citations, context citations and use status.
4. Include matching original assertions with applicability, exclusions, witnesses and answer/execution restrictions; linked findings with all counterevidence and remaining questions; and the selected report section's required facts/dependencies, disposition and limitations. Avoid importing every report section merely because it shares `planet-lexicon`.
5. Preserve the chapter PHDDASR order and the competing lexicon order in the evidence. Sign computation occurring earlier is distinct from the selected interpretation sequence.
6. Bound question roots or output detail before packet construction; never silently prune contradictory witnesses to fit a token budget. Too broad a question can receive a scoped overview plus a useful follow-up.

Manifest `authorities` entries declare fixed `path`, `sha256` and `hash_normalization="UTF8_UNIVERSAL_NEWLINES"`. Reproduce the export generator's normalization exactly:

```python
normalized = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')
```

Compare that SHA256 for every canonical authority actually used, including concepts/assertions/findings/requirements/meaning profiles and any sent annotations/reviews. `component_use.sha256`, generated topic-packet and bundle hashes instead cover their exact generated bytes. Fixed expected filenames prevent a modified manifest from redirecting reads elsewhere. Record the raw manifest hash plus normalized authority hashes in each response/export. A hash match proves consistency with the declared local manifest, not source completeness, empirical validity or resistance to coordinated replacement of every authority.

The deployed `data/**` package contains the canonical JSON. No private PDF, image, OCR or SQLite access is required for this portable retrieval path. Media remain private and their exact witness hashes stay attached.

## Practical per-claim safeguards

An answer-level source list alone does not prove each sentence. A useful writer/reviewer result includes a small claim ledger: claim kind (`calculated_fact`, `conditional_component_reflection`, `source_explanation`, `practical_option`), actual fact references, source IDs and stage references. The server should reject missing references, unavailable house/angle facts, invented sources, unsupported timing epochs and attempts to alter trusted chart/approval metadata. Render numeric coordinates and fact labels from server data rather than trusting model-generated numbers.

A second model review is an additional safeguard, not a complete deterministic semantic proof. Adversarial checks should include a writer/reviewer that fabricates a citation, invents biography, changes a fact, merges Eunomia alternatives, substitutes generic Chiron meanings, or calls incomplete directed geometry a completed method. Missing degree/aspect stages must not be cited as evidence for a complete conclusion. Neither model can promote a source rule's approval status.

Current-epoch geometry must remain a separate dated layer. A fixed natal-house overlay is not a moving event Ascendant. A snapshot does not establish orb entry/exit, exact interval peaks, stationary touches or all retrograde repeat passes. An answer can discuss available dated facts and explain a particular missing timing calculation without declaring every question unanswerable.

## Evidence inspected

- `knowledge_audit/report_components.py`: actual component-use contract and annotation behavior.
- `scripts/export_report_knowledge.py`: normalized fingerprints, source authorities, topic dependency closure, assertion/finding retention and portable-media boundary.
- `data/knowledge/{interpretive_inventory,original_assertions,source_blocker_findings,material_requirements,source_meaning_profiles,report_knowledge_manifest}.json`: current schemas and selected context/profile records.
- `api/index.py`, `vercel.json`, `.env.example`, and the current `AGENTS.md`: existing application protection, time budget and preservation policy.

This research did not independently inspect every original scan, validate model answer quality or test a live DeepSeek key.
