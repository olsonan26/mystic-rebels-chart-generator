# NADIA profile report candidate

Branch codex/nadia-profile-report-20261104 starts from exact Phase8 head e704e8cb62194c3a979bada55eed395b3ff03253. It is a stacked report change, not a merge of Phase8 or unrelated application history.

## Run locally

Use the existing Python dependencies and ephemeris assets. Install the immutable private0.7.0 wheel using docs/NADIA_PRIVATE_INTEGRATION.md. Start `python -m uvicorn api.index:app --host 127.0.0.1 --port 8000 --no-access-log` and `npm run dev`. Open http://127.0.0.1:5173. Click Load synthetic example, then Generate profile. Choose Essential or Premium, Download JSON, or Print / save PDF. Booking appears only when the owner supplies a valid HTTPS NADIA_BOOKING_URL. No payment processing is added.

POST /api/profile-reports accepts birth (existing BirthInput), tier essential/premium and synthetic boolean. It recalculates all ten major bodies and required angles. Schema nadia-profile/1 separates chart facts, source vocabulary, rule/source dependencies, evidence, blockers and readiness. All18 established interpretation sections remain unavailable for complete personalized conclusions; ten verified function-context components can be displayed. Premium has the same currently approved scope; no filler is invented.

Source content comes only from the integrity-verified pinned private library. Failed verification yields calculated facts with an explicit source-unavailable state, never legacy or generic fallback. Missing/approximate time suppresses houses, angles, Field and Delegate context. The report has deterministic identity and JSON for identical input and installed core, with no wall-clock timestamp. The lead question requires whole-chart/ruler/occupant/condition context; its answer stays null and asks a reflection question.

Reports are request-memory only, no server or browser report persistence. Existing site password middleware protects deployed routes; POST checks origin and no-store headers. Development loopback proxy is permitted only outside Vercel. Exports include birth details. Reflection is excluded from export and print. Do not enable public preview without the established private-build and authenticated deployment prerequisites.

## Verification and limits

476 complete backend/access tests pass with zero skips, including13 new API/calculation/gate tests against installed private core.44 frontend tests pass. Production Vite build and private browser-boundary scan pass. Browser verified synthetic birth entry and real chart rendering, then discovered a local proxy-origin error; fixed and API regressions passed. Browser control was subsequently disabled in Work settings, preventing final visual report/JSON download/PDF-dialog verification. Print/savePDF is implemented but actual PDF output is not verified. A local synthetic sample is retained at ignored tmp/nadia-profile-synthetic.json; it is not committed to the public repository because it contains private-core source vocabulary.

Complete comprehensive interpretation is NOT ready. Private core reports/PROFILE_REPORT_CRITICAL_PATH.json reconciles207 requirements/18sections/131concepts and separates natal foundations, applicability-dependent extensions and specialized contexts. Essential gaps include degree/Spark/FCA authority, full body-angle/contact boundaries, complete related conditions and contextual meaning, articulation, source-based personal-context application, motion overlap/equality and progressed applicability. Source audit now85 complete chapters/271reviewed witnesses. No new runtime authority or version was activated. The engine remains0.7.0; consumer production/Preview not deployed.
