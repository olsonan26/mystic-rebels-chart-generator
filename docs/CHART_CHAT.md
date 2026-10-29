# Chart conversation after generation

Implemented 28 October 2026 in the main Mystic Rebels chart generator. Generate a chart, explicitly load the example, import chart JSON or reopen a saved chart: the conversation panel opens with **“What do you want to know?”** The initial automatically displayed example offers a launcher without opening the panel. Typed questions and follow-ups are supported; answers are generated rather than chosen from four canned topics.

**Production release:** deployed at the owner's request on 28 October 2026 to [the existing protected site](https://www.cosmodynamicschart.site/). [Deployment receipt and verification scope](CHART_CHAT_DEPLOYMENT_20261028.md). Build, source integrity, aliases and anonymous access checks passed; the owner explicitly chose to skip an authenticated production chat test. Local real-provider/browser validation remains the evidence for the full conversation flow.

## Run and connect

Add the following to the server's ignored `.env` or intended hosting environment. The template contains no working credential:

```dotenv
OPENROUTER_API_KEY=
OPENROUTER_MODEL=deepseek/deepseek-v4.1-flash-1017
```

Install `requirements.txt`, run `npm run build`, then run `python scripts/run.py` using the documented local runtime. Open `http://127.0.0.1:8000`, generate a chart and type a question. The owner-selected OpenRouter connection is configured locally and on the existing Vercel project's Production environment. A different host needs its own environment configuration and deployment.

The browser sends birth-input context, its chart fingerprint, the question, the last 20 user/assistant messages and the requested sky date to the application server. The server reconstructs trusted positions and sends these, reviewed source evidence and conversational context to OpenRouter for writer and separate reviewer passes. Credentials stay in the server environment. They are excluded from Git, downloads and recovery archives. The existing hosted `SitePasswordGate` wraps the new routes too.

`GET /api/chart-chat/status` reports connection availability without revealing credentials. `POST /api/chart-chat` generates a reviewed reply. `POST /api/chart-chat/context` calculates inspectable evidence without a paid model call, so **See chart context** works independently of model connection availability. The normal chart-generation route remains separate.

## What the answer uses

- Trusted natal calculation bound to the generated chart fingerprint. Core physical planets and Chiron are included even when hidden on the wheel; explicitly named catalog objects are calculated where available. Ambiguous node/Lilith/Sophia variants remain separately identified.
- Planet → House → Degree → Decan → Aspects → Sign → Ruler assessments, followed through actual rulers with cycle references. A structural ruler lookup does not claim complete Delegate condition or a final dispositor. All 12 resolved Whole Sign sectors are represented, including unoccupied ones. Unknown birth time withholds houses/angles.
- Question relevance from explicit houses, transparent topic/lexical matching and actual natal factors. This is a retrieval plan, not a strength ranking. Short follow-ups retain the preceding user topic; prior model statements are never promoted into chart facts.
- Manifest-checked source authorities, complete selected concept/profile/assertion dependency closure, competing witnesses, linked findings and applicable requirement contracts. Nothing changes canonical source-use or full-report approval flags. The chapter's sequence and lexicon sequence variant remain in the packet. Chiron retains Fractured Structures; Eunomia retains both alternatives; Sun/father and Moon/mother remain symbolic conventions rather than biography.
- Reviewed natal component reflections, source explanations, measured chart facts and practical options. Each visible paragraph has a typed claim and actual source/fact/stage references. A second model pass reviews the draft; structural checks reject invented references, unsupported reflective stages and attempts to override approval gates. Current-sky fact paragraphs are rebuilt directly from trusted positions, rather than trusting generated interpretations embedded in those paragraphs.

**Why this answer?** exposes seven stages, ruler routes, used meanings/exceptions/citations and the dated sky view. Downloads retain claim references, chart facts and source/context fingerprints. Reference checks and a separate AI review improve traceability; they cannot prove semantic accuracy or empirical validity. These are bounded component consultations, not an approved complete personal-report engine.

## Current sky and aspects

**Include the current sky** defaults on. Use **Now** or select a date/time explicitly labelled UTC. Each reply preserves its own resolved epoch. This is a requested snapshot, not a continuously refreshing ticker. Available core sky points and named physical catalog bodies are geocentric calculations with motion and fixed-natal-sector overlays. Current-location houses are not guessed.

The explanation shows actual sky positions/motion and angular separations to natal positions. Its closest diagnostic-angle matches are explicitly geometry, not author-qualified aspects, influence rankings or accepted orbs. The evidence also retains sky-to-sky geometry. Full directed OOI, receiving/Delegate condition, Spark meaning, complete event searches, progressions and forecast timing remain incomplete. A question requiring those receives supported information and a specific limit; “any question” is an input affordance, not a promise of a certain answer or prediction.

## Saving and recovery

Each chart's exact question/reply history and unsent draft are versioned in this browser's local storage, separately from Supabase. Display-object and wheel changes retain that conversation. Changing birth identity isolates it; in-flight requests are aborted on chart replacement. Failed questions remain available to retry. Saving is debounced, with immediate page-hide/visibility/unmount flushes. A quota failure displays a download notice.

**Download conversation** creates a standalone JSON packet containing birth input, every exchange, each answer's evidence/source hashes, timestamps, the unsent question and selected sky settings. New answers append rather than replacing previous answers. Browser reload/reopening the same chart restores its local history. A downloaded JSON file is independently readable; a conversation-import UI is not implemented. Browser storage alone is not a durable off-device backup: download important consultations to a private location.

Code, research, tests and knowledge exports are committed and pushed under the [GitHub preservation agreement](GITHUB_RECOVERY.md). Private consultations are not automatically published to the public source repository. The existing private recovery release preserves source media and earlier dirty working files; the feature checkpoint adds committed code history. The inaccessible live Supabase database remains a separate export gap. No automatic all-customer or automatic per-message GitHub backup is claimed.

## Validation and continuation

All **414 backend tests** and **138 frontend tests** passed; the production build passed. Focused backend tests exercise real ephemeris/source context, source hash tampering and dependency closure, unknown birth time, chart identity, ruler cycles, dated overlays, ambiguous Eunomia meanings, hostile writer/reviewer outputs, fixed outbound routing, provider failure redaction and truncated/invalid responses. Frontend tests cover chart isolation, versioned recovery, corrupt evidence and history limits. Real OpenRouter calls use fictional charts only. [The verification receipt](../evidence/chart-chat-verification-20261028.json) distinguishes the real provider/browser reply from mocked follow-up/error checks and records the tested local scope.

`scripts/verify_chart_chat_browser.cjs` reproduces the browser flow against a running local server. It requires Playwright with Chrome available and explicit `RUN_LIVE_CHAT_QA=1`, because it makes one real fictional paid request. `PLAYWRIGHT_MODULE` can point to the desktop runtime's installed Playwright package when it is not installed in the project. Debug transcripts, exports and screenshots are written only under ignored `tmp/`. No account/saved-chart cloud access or deployed customer flow was independently verified.

Remaining work: complete the prioritized primary-source method gaps in [the audit](research-20261028/DEEP_AUDIT_AND_NEXT_STEPS.md); add a deliberate private consultation import/sync/export service if desired; obtain authorized live database exports; verify the deployed authenticated conversation/customer path when the owner requests that check. Deployment readiness and protected public responses do not establish a successful production model reply.
