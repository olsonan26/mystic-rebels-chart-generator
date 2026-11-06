# Bounded NADIA Profile Generator

The existing chart-to-report flow now produces a usable bounded chart profile,
with a chart wheel, ten-major placement overview, scoped Sun/Moon context,
verified source-scoped contacts, optional evidence appendix and a local review
brief. It reuses the calculation service, report endpoint, immutable private
core 0.7.0 and existing source-eligibility checks. No new model, calculation
engine, knowledge release, architecture or source audit is required by this change.

## What the finished flow does

Enter birth details, choose a birthplace, generate the chart, then choose
**Generate profile**. For a town missing from the city catalogue, open
**Coordinates & time zone**, enter the birthplace label and coordinates, and
resolve its time zone with the existing polygon lookup. The report labels time
precision and coordinate limitations; a city reference is not an exact birth site.

Read the chart overview, inspect a chart object, explore the two source-defined
functions and their calculated context, and inspect verified contacts. Occupied
house, represented houses, own motion and house-channel ruler remain distinct.
Reflection prompts are questions, not chart-derived personal conclusions.

**Download JSON** preserves the complete report evidence and unknowns.
**Print / save PDF** exports the visible report; opening the optional supporting
appendix includes that evidence in print. **Download review brief** creates a
human-readable checklist tied to the report identity. It submits nothing and
does not approve an interpretation. Share that file and the report JSON with a
qualified reviewer deliberately. No booking destination is invented.

## Gates and actual scope

`complete_personal_reading=false`, `interpretation_status=blocked` and the null
personalized lead answer remain unchanged. Every guide item comes from an
already eligible report component; none permits personal inference. The new
review record is required, unsubmitted and unapproved. There is no client-side
approve button, model writer or reviewer bypass. Qualified review must still
respect unresolved source rules; review alone cannot create missing authority.
The product is complete within this bounded scope, not a complete personal
interpretation engine or paid-reading approval.

Missing private-core integrity yields facts without a source guide. Missing or
approximate birth time suppresses houses, angles and derived house context.
Reflection notes are not transmitted, persisted or exported. Reports remain
request-memory only. Access, origin, private-package, source, release and
deployment protections remain in force.

## Verification on 5 November 2026

- 494 existing backend/calculation/access tests passed, no skips; includes new
  component-provenance, unknown-time and unapproved-review checks.
- 47 frontend tests passed; TypeScript/Vite production build passed.
- Private package/browser boundary and `git diff --check` passed.
- Real local API/Chromium flow passed for the owner's supplied real chart:
  birth entry, manual town coordinate/time-zone resolution, chart generation,
  profile, object selection, JSON/review downloads, both PDF variants, mobile
  layout and return to chart. No external requests or browser exceptions.
- Synthetic regression flow passed on desktop/mobile, uncertain time and long
  names, birthplace selection, safe booking configuration and reflection privacy.
- PDF inspection checks names, page bounds, vector charts, expected appendix
  visibility and reflection exclusion. Actual images were separately inspected.

Known environment limitations: the consumer `.venv` lacks Swiss Ephemeris.
Local calculation checks and API therefore used the already installed
`../Mystic-Rebels/.runtime/python.exe` (Python 3.11), not a new installation.
The deployment dependency specification remains Python 3.12; no hosted build
or deployment is claimed. Existing Vite chunk-size and Starlette dependency
deprecation warnings remain. No protected branches were merged or deployed.

## Reproduce locally

Use an existing compatible Python environment with the documented dependencies
and verified pinned private core. `python scripts/run_profile_local.py` starts
the existing protected API on loopback8000. `npm run dev` starts the existing UI.
The verified session used loopback5175 because the default port was occupied.

```powershell
node node_modules/vite/bin/vite.js web --host 127.0.0.1 --port 5175 --strictPort
npm test
npm run build
python -m pytest astronomy_qa access_qa -q
python scripts/check_nadia_boundary.py
```

Set `NADIA_PLAYWRIGHT_MODULE` and `NADIA_CHROMIUM_EXECUTABLE` to already-installed
Playwright/Chromium when necessary; `NADIA_TEST_URL` selects the local UI port.
`node scripts/verify_profile_browser.cjs` runs the synthetic regression.

For a real-chart demonstration set `NADIA_PROFILE_BIRTH_FILE` to a private local
JSON containing `name`, `local_date`, `local_time`, expected IANA `timezone`, `birthplace_query` and
`birthplace_match`. Optional `coordinates` (`latitude`, `longitude`) and
`location_name` exercise manual entry. Run:

```powershell
node scripts/verify_profile_product.cjs
python scripts/verify_profile_pdf.py --product
```

Private inputs, PDFs, JSON, review brief, screenshots, video and exact run
receipts stay under ignored `tmp/profile-product` and `tmp/nadia-profile-birth.json`.
Do not commit them to this public repository. Their recovery destination is the
separately verified private recovery repository. Public preservation includes
only product code, synthetic/generic tests and this scope record.
