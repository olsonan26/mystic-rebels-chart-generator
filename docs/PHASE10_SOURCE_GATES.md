# NADIA — Phase 10 source gates and Gradity-specific book review

## Source priority and scope

The currently deployed chart's astronomical backend, unrounded longitudes, Whole Sign houses, True Placements, JSON export and named PURE ASTROLOGY transformations are **not changed** in this branch. This is a frontend presentation and research-contract refinement. The GitHub base branch is `codex/dual-wheel-refinement`, not the older `main`. No source PDF or author page photography is added to this repo.

## Position and sign layers

The numeric `Position` column projects `formatPosition(longitude, precision).split(" ")[0]`. Thus the degree/minute/second values are exactly the same as before, while the zodiac text is removed **only from the Position table cell**. Astronomical Sign/Tone is explicit in a separate column, and True Placement/Field and Whole Sign house remain separately visible. The raw `longitude_deg` and existing full-sign object hover remain untouched.

## Gradity — newly verified directly from PURE ASTROLOGY

- **Printed p207, Retrograde Planets:** exactly four Gradities are **Prograde**, **Pregrade**, **Retrograde**, **Postgrade**. Stations are turning/inertial conditions, **not** fifth/sixth Gradities.
- **Printed pp479–480, Totally Retro:** stationary directional changes are *Inertial Points*; a day on each side is highlighted qualitatively, **not** a numerical station speed tolerance.
- **Printed p569, Retrograde Imprint Theory:** Pregrade begins after passing the *degree where upcoming retrograde will end*; Retrograde revisits previously traversed degrees; Postgrade ends at the *degree where retrograde began*.
- The astronomical speed sign supports observed Direct or Retrograde motion. Exact zero supports a mathematical instant `Stationary`; no arbitrary near-zero threshold is source-established.
- **Pregrade/Postgrade** cannot be assigned until the actual four timing events have been calculated and validated; a signed speed alone is insufficient. The research-only event-based classifier returns `null` at undecided exact boundaries. For forward motion outside a verified loop the chart displays `Unverified`, not a fabricated `Prograde`.

## Phase 10 explicitly permitted versus blocked

| Phase 10 finding | Status | Applied behavior |
|---|---|---|
| Genuine object longitudes and numerical DMS | READY by prior astronomy work | preserved unchanged; number and sign displayed independently |
| Modern triplicity decan ruler ring / true placement ring | READY visual layer | preserved from current base branch |
| All-object anchors with collision-limited labels | Presentation-only | exact anchor remains, annotation may be omitted and is found in table |
| Moon crossing shared Mars-Saturn Fringe pp240–242 | VERIFIED_EXAMPLE only | retained for future source-specific research diagnostics, not generalized to all aspects |
| Spark parity H versus Z | CONTRADICTED | production Spark remains disabled |
| Universal outgoing OOI list and all aspect rules | BLOCKED | no invented values or general aspects |
| FCA 1°30′ / 30′ / 3′ approaching widths | RESEARCH READY | no weight or changed primary house assigned |
| 2°,32°,62°,92° cyclical age labels p255 | VERIFIED_EXAMPLE | not converted to exact dated prediction without chart context |
| Complete return/progressed/current-life interpretation | BLOCKED | no prediction generator enabled |

## Implemented Phase 10 research-only helpers

`web/src/phase10Research.ts` contains separately tested **approaching-only** three-scale FCA proximity (including 10°57′ within 3′ and 5°56′ outside), **integer-degree undated age labels** (2, 32, 62, 92), and both disputed house-/sign-parity Spark candidates with `canonical:null`. These diagnostics are not enabled as interpreted readings, do not mutate object records and never produce prediction dates. The entire advanced-aspect mechanism remains blocked.

## Visible regression requirements

- Exact numerical `longitude_deg` remains stable for chart markers, table-row data attributes and exported chart JSON.
- Core / expanded / research all-object density is controlled by existing sparse/balanced/detailed/all modes, not silently dropping selected markers.
- Every label is within 24° of its exact marker; if the available track slots fill, the marker stays and the annotation is omitted. Labels have deterministic priority, then longitude ordering.
- Motion and Gradity are separate columns and chart inspector properties. Unsupported phase claims remain `Unverified`.

## Release caveat

The Astro-team Vercel project reports no *native* Vercel password/SSO protection, but the repository includes custom HMAC-signed access middleware and protected API routes (see docs/SITE_ACCESS.md). Verify the live password gate and environment configuration before claiming a public or private access state. The existing Swiss Ephemeris AGPL/professional licensing decision remains separate. This patch changes neither licenses nor astronomy binaries.
