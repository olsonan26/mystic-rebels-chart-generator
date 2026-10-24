# Mystic Rebels compact Dual wheel

This changes presentation only. The existing Swiss calculations, object catalog, coordinates, Whole Sign assignments, True Placements, Tone/Pulse/rulers, mathematical Parts and interpretation outputs remain unchanged. No aspect lines or new astrological procedures were added.

## Concentric architecture

| Band, outside to inside | SVG radius |
| --- | --- |
| Degree scale; 10-minute subdivisions at 200% zoom | 474–486 |
| Tropical astronomical zodiac | 432–468 |
| Modern triplicity decan-ruler glyphs | 410–432 |
| Exact astronomical markers | 400 |
| Collision-managed glyph/position annotations | Between energy and marker bands |
| House-derived True Placement energies | 183–224 |
| Selected/hovered object inspection | 0–168 |

All 36 decan legend entries are checked against references recorded from the existing placement rules before changes. The legend does not recalculate or replace any point's interpretation fields. The inner energy track remains house-derived: house 1 Aries, house 2 Taurus, and so on, independently of the external astronomical sign.

Ascendant alignment retains the existing rotation. Whole Sign boundary alignment uses 0° of the rising astronomical sign at the left horizontal axis. Both use the same point records, same independent AC/MC and same Whole Sign cusp boundaries. A point's unrounded longitude always determines its marker; collision handling changes annotation positions only.

## Dense charts and access

Sparse, Balanced, Detailed and All that fit control annotations. Selection, search matches and major objects have priority. Spatial hashing and deterministic tie-breaking pack text without changing the input arrays. Finite label capacity never throws a chart-capacity error or removes a marker. The center reports the marker and annotation counts; the help text states that reduced labels do not mean reduced positions. Coincident astronomical longitudes remain coincident; search, keyboard focus, selection and the complete table distinguish their objects.

Zoom extends to 400%, with normal horizontal/vertical viewport scrolling. At 200% the scale adds 10′ subdivisions. Search covers every successfully calculated object in the chart, highlights matching markers and prioritizes its label; it does not filter the astronomical point set. Hover previews and keyboard focus show details centrally; selection also updates the existing inspector.

The original renderer is retained as `LegacyWheel.tsx` and remains selectable with Layout → Original (rollback). Its numerical data and original Ascendant alignment are retained. This also provides a visual comparison without reverting the application.

## Numerical and visual evidence

The immutable `evidence/wheel-refinement/before.json` was captured from commit `e250662` before changing the renderer: four charts, 296 point records, and 36 decan references. `scripts/wheel_regression.py` verifies every calculation/interpretation/export field and hashes every engine source file plus the manifest/catalog. `git-source-baseline.json` records source hashes from that original Git commit. Engine bytes must match exactly; only the manifest's CRLF/LF text encoding is normalized for its independent content check. Cross-environment comparison excludes generation timestamps, Python runtime-version metadata and the platform-dependent raw manifest file fingerprint; no floating-point tolerance or rounding is applied to calculated fields.

- All engine source files are byte-identical. Catalog and manifest content match the original Git commit; Git line-ending normalization is accounted for separately from content.
- All 296 point records, houses, derived placements, rule metadata and numerical export fields match the baseline exactly.
- 238 existing astronomical/API checks and 13 frontend checks pass. The frontend suite includes both alignment modes, all 36 modern decan legends, original-renderer rollback, exact markers and a synthetic 500-object stress case.
- Actual browser JSON downloads from the compact and original designs are byte-identical. Both downloaded SVGs contain the same 72 unrounded object-coordinate pairs. SVG appearance intentionally differs; text styling is embedded for standalone use.
- Whole Sign SVG marker-coordinate inversion differs from recorded longitude by at most 4.10e-10 arcsecond, from floating-point trigonometry only; stored longitudes do not change.
- In the measured 72-object chart at 100% Whole Sign view, All that fit places 61 non-overlapping text labels while retaining 72 markers and 72 table rows. At 200%, all 72 labels fit. Counts vary with chart clustering, selection, search and zoom.
- REA desktop (1440×1640) and mobile (390×844) workflows complete without captured page errors. These are browser viewport checks, not claims of testing every physical phone/browser.

Evidence: `numerical-regression.json`, `browser-regression.json`, `compact-export.svg`, REA captures and `compact-desktop.png` / `compact-mobile.png`, all under `evidence/wheel-refinement/`.

The 500-object case is a synthetic presentation stress test. It does not expand the production catalog or claim calculations for unsupported objects.

## Hosting destination

The supplied Vercel account is the Astro team (`astro-ac32`). Project: https://vercel.com/astro-ac32/mystic-rebels-chart-generator. Site: https://mystic-rebels-chart-generator-seven.vercel.app. Deployments require Vercel authentication. The previous account's deployment is retained for rollback.

The source remains in the existing private GitHub repository. The Astro account cannot currently access that private repository through its Vercel Git integration (`repo_not_found`); deployment uses the authenticated CLI against the same checkout. Automatic Git deployment in Astro requires granting that Vercel account access to the repository. No new repository or calculation engine was created. No privileged account tokens are included in code, artifacts or browser configuration.
