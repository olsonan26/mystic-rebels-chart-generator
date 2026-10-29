# Mystic Rebels — Alchemystic Astrology Chart Generator

**Latest source, PHDDASR and current-transit review:** [28 October deep audit and next steps](docs/research-20261028/DEEP_AUDIT_AND_NEXT_STEPS.md). The separate local prototype has partial ordered assessments; typed questions and a current-transit consultation view are still missing from the main chart generator.

**Keep the work recoverable:** [GitHub preservation and restore guide](docs/GITHUB_RECOVERY.md). Code and knowledge use this repository; raw private sources and recovery assets use the separate private recovery repository. Live database exports have their own explicit access/verification status.

**Looking for meanings or report knowledge? Start with [REPORT_KNOWLEDGE_START_HERE.md](REPORT_KNOWLEDGE_START_HERE.md).** Read branch `codex/methodology-verification-20261024`; the default `main` snapshot predates the interpretation audit. [Open the knowledge branch on GitHub](https://github.com/olsonan26/mystic-rebels-chart-generator/tree/codex/methodology-verification-20261024).

**Use the audited source instead of an existing library:** [the updated component guide](docs/REPORT_COMPONENT_USE.md) includes all12 original sign core entries, Chiron's Fractured Structures vocabulary and both Eunomia alternatives. There are60 vocabulary annotations plus one explicit alternatives output. Generic-library fallback is forbidden; unresolved source claims stay visible. Run `python scripts/annotate_chart_sources.py examples/report-source-input.json --format markdown` for the tested consumer.

Saved knowledge: **131 concepts, 267 selected assertions, 207 report requirements and 50 findings**, with contextual vocabulary for planets, houses, sign/decan/degree layers, cusps, asteroids and aspects. [The machine manifest](data/knowledge/report_knowledge_manifest.json) points to a complete bulk export and seven smaller topic packets for external ingestion. Preserve exceptions, citations, dependencies, conflicts and approval gates. This is partial source-grounded knowledge; all 18 report sections remain unready for personal reports.

Current source-audit checkpoint: [closing chapters, BTR and lexicon](docs/2026-10-25_source-audit-closing-btr-continuation.md). **725 targeted images; 267 assertions; 10,245 checked OCR locators; 304 images and 23,781 locators remain**. [The master knowledge path](docs/PROFILE_REPORT_KNOWLEDGE_PATH.md) indexes all retained work. Counts in older documents are historical. This export adds no runtime interpretations or deployment.

Independent Mystic Rebels web application with a native Swiss Ephemeris calculation API, precise SVG natal/Dual wheels, grouped object selection, a full-precision position model, and Supabase account/saved-chart integration.

Repository: https://github.com/olsonan26/mystic-rebels-chart-generator

## Run the installed application on this Windows machine

```powershell
cd 'C:\Users\olson\OneDrive\Documents\Reverse Skill\work\Mystic-Rebels'
npm ci
npm run build
.\.runtime\python.exe scripts\run.py
```

Open http://127.0.0.1:8000. `Load example` loads the documented illustrative Los Alamitos chart. This is labelled Example chart; its coordinates are editable and are not represented as a certified individual birthplace.

For frontend development run `npm run dev` in a second terminal. Vite proxies `/api` to the same Python API on port 8000.

## Fresh installation

Linux/macOS or a normal Python 3.12 installation:

```sh
python -m venv .venv
# Activate .venv using the command appropriate to your shell.
python -m pip install -r requirements-qa.txt
npm ci
python scripts/provision_ephemeris.py
npm run build
python scripts/run.py
```

On Windows, the upstream pinned binding supplies CPython 3.11 wheels. `scripts/bootstrap_runtime.py` installs an isolated official CPython 3.11.9 embedded runtime. Install dependencies into it with a recent system pip: `python -m pip --python .runtime/python.exe install -r requirements-qa.txt`. The Windows runtime is used only for development; Vercel is explicitly configured for Python 3.12. Never install the binding into a different existing application environment.

Pinned official ephemeris files and the compact offline place index are included in the private repository. The executable provisioner verifies SHA256 and downloads missing files from recorded official/vendor-published URLs. `data/ephemeris-manifest.json` records origins, exact sizes, retrieval times, and hashes. `scripts/provision_locations.py` regenerates the compact location dataset from the pinned development dependency.

## Verify

```powershell
.\.runtime\python.exe -m pytest astronomy_qa -q
npm test
npm run build
.\.runtime\python.exe scripts\validate_horizons.py
```

The last command performs live NASA queries and stores raw responses. Ordinary tests use the saved independent reference data without network access. Historical research checks remain unchanged in the private input package; their 87 checks are separately recorded in `evidence/research-87.xml` and are not counted as new astronomical validation.

## Hosting

The Vite frontend and `/api/index.py` ASGI calculator deploy together on Vercel. Current destination: [Astro project](https://vercel.com/astro-ac32/mystic-rebels-chart-generator), [authenticated site](https://mystic-rebels-chart-generator-seven.vercel.app). Source stays in the existing private GitHub repository. The Astro Vercel account still requires access to that private repository for automatic Git deployment; the authenticated CLI deploys the same checkout in the meantime. `vercel.json`, `.python-version`, and `pyproject.toml` configure the native Python function and data inclusion. The compact GeoNames index avoids shipping the much larger development database package in the function.

The compact wheel adds concentric bands, modern decan glyphs, selectable Ascendant/Whole Sign boundary alignment, label density, chart search, central hover/selection details and zoom up to 400%. Layout → Original retains the previous renderer for rollback. See `docs/WHEEL_REFINEMENT.md` for the unchanged numerical snapshot, real export comparisons and dense-object validation.

Alchemystic Astrology is the astrology system's name; Mystic Rebels remains the brand. The decorative purple plasma orb beside the heading includes pause and reduced-motion support and stays separate from all chart calculations.

Set `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY` in each intended Vercel environment. Only the publishable key is exposed by `/api/config`. No service-role key is required by the client or calculation API. Local values go in ignored `.env`; see `.env.example`.

Apply `supabase/migrations/20261024100237_mystic_rebels_charts.sql` to the intended project using an authenticated project administrator. The table uses ownership checks and RLS for all read/write operations. Until schema application and live verification are completed, cloud saving is not a verified completed capability.

Keep deployments authenticated until numerical acceptance and the Swiss Ephemeris release license are resolved. The official vendor requires choosing its AGPL-compatible or professional licensing route before distribution/public service activation. This private development repository does not imply a purchased professional license. See `docs/PRECISION.md` for actual measured numerical agreement and release limitations.

## Knowledge foundation and method verification

The current product is a chart generator, not a complete source-grounded personal-answering system. See `docs/KNOWLEDGE_ARCHITECTURE_AUDIT.md` for the eight-batch audit status, actual runtime gaps, source conflicts and implemented evidence controls. `data/knowledge/capabilities.json` separates historical readiness, implementation, retrieval and personal-answer approval; `/api/methodology` returns metadata through the existing access boundary.

`python scripts/knowledge_audit.py check` validates that register without claiming full source coverage. A private local source index can be built with `python scripts/knowledge_audit.py index-pdf reference/source_pdf/PURE_ASTROLOGY_Nadia_Complete.pdf --source-id pure-reflow-9d5fb55c`; `python scripts/knowledge_audit.py search "odd numbered houses"` returns page/hash witnesses. The index stays in ignored `reference/` and is not deployed. Search hits are not approved interpretations.

Gradity now solves real station/shadow events with the current engine and retains unassigned exact boundaries or overlapping-shadow conflicts. See `docs/astronomy-followup.md` for independent Mercury/Venus sample comparisons and their limits. `python scripts/methodology_regression.py` checks established point values against the archived engine on the same runtime; the original presentation-only byte-identity script and immutable fixtures remain for historical rollback.

## Input data and privacy

The interpretation continuation is in `docs/INTERPRETIVE_COVERAGE_AUDIT.md`, with a readable 127-record appendix in `docs/INTERPRETIVE_INVENTORY.md`. `python scripts/knowledge_audit.py check-semantics` validates meaning/exception/example provenance; `profile-gaps --section parts-profile` expands report prerequisites; `concept spark-entry --section profile-foundation` retrieves all cited local witnesses including counterexamples. These are audit tools, not production personal reports. Full original-batch completeness remains unestablished.

The calculator does not persist birth data. Chart responses are `no-store`. Saving a chart is an explicit signed-in action. The source PDF and historical reference directory are excluded from Git and deployment. Geographical search uses GeoNames city centroids in WGS84, with attribution to https://www.geonames.org/ under CC BY 4.0. Users can enter more precise coordinates; a city centroid is not an exact individual birth location.
