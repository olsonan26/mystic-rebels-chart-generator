# Mystic Rebels astronomical validation

Verified 2026-10-24. Numerical reproducibility, agreement with a reference model, and uncertainty in the actual birth data are separate quantities. No claim of infinite physical accuracy is made.

## Installed calculation model

Swiss Ephemeris C 2.10.03 through pinned `pyswisseph==2.10.3.2`; tropical, geocentric, apparent ecliptic/equinox of date. Planetary-system barycenters follow Swiss defaults. Production flags are `SWIEPH | SPEED` (258). Each ecliptic and equatorial calculation checks the returned ephemeris mask, rejecting Moshier or JPL fallback. Angles are explicitly identified as geometry and Parts as derived points.

The 44 installed official/vendor-published assets total 13,647,054 bytes. `data/ephemeris-manifest.json` contains the exact source URLs, UTC retrieval times, byte sizes, SHA256 hashes, and vendor Git revision. Core planetary, lunar and main-asteroid files are included alongside all 40 additional catalog bodies. Hashes are checked before calculation. Missing, corrupt, unsupported or out-of-range objects produce explicit unavailable results; no substitute longitude is generated. Core dates are limited to 1800–2399 UTC; additional numbered bodies to 1800–2099 UTC.

Civil time is resolved with pinned `tzdata==2026.5`, including explicit ambiguous-time fold selection and rejection of skipped local times. UTC is converted to TT and UT1 using `swe.utc_to_jd`; both Julian dates, Delta T, IANA zone, offset and package versions accompany the result. Historic Delta T and local civil records have uncertainty. Future leap seconds and future legal timezone changes cannot be predicted exactly by a pinned database.

The place search contains 34,006 GeoNames city locations in WGS84. These are city centroids, not a certified individual's birth coordinates. Coordinates and timezone can be edited. Unknown birth time uses an explicitly labelled local-noon reference, with angles, houses and dependent placements suppressed.

## Independent results

`evidence/independent-astronomy.json` and raw responses in `evidence/horizons/` record 165 NASA JPL Horizons comparisons: 55 physical bodies at three epochs (1992-07-18 03:01 UTC, 2000-01-01 12:00 UTC, 2024-04-08 18:00 UTC). No Astro.com chart-generation service is used.

Reference matching uses Earth geocenter `500@399`, the appropriate planetary-system barycenters, and ICRF astrometric coordinates with light time only. The diagnostic Swiss flags also disable aberration, solar deflection and nutation and select ICRS/J2000 equatorial coordinates. This diagnostic comparison does not change production apparent coordinates. RA differences are weighted by cos(declination) when calculating sky separation.

| Measured quantity | Largest residual in these samples |
| --- | ---: |
| Ten major bodies, matched ICRF sky separation | 0.001238315 arcsecond (Mercury) |
| Moon, matched ICRF sky separation | 0.001077517 arcsecond |
| All 55 bodies, matched ICRF sky separation | 0.898813244 arcsecond (Hygiea) |
| All 55 bodies, apparent ecliptic longitude | 1.222630364 arcseconds (Pallas) |
| Local Windows vs hosted Linux, all 72 enabled longitudes | 0.0 arcsecond |

The apparent ecliptic comparison deliberately retains the documented precession/nutation-model and minor-body orbit-solution differences between the two providers. Pallas's longitude residual exceeds one arcsecond at the 2000 epoch; its matched ICRF sky separation is 0.862955706 arcsecond. This result is retained, not rounded away or represented as universal subarcsecond apparent-longitude agreement. These sampled results are not validation of every date or a guarantee that an uncertain asteroid orbit is physically exact.

Independent ERFA/IAU geometry checks cover AC/MC at seven locations and three epochs, plus high latitudes, the Vertex prime-vertical intersection, opposing angles, spherical Nonagesimal geometry and singular horizons. AC/DC and MC/IC remain independent of Whole Sign cusp boundaries; MC is not forced into house 10.

## Executed checks and precision path

- 238 independent astronomical/API checks passed (`evidence/astronomy-qa.xml`), including the 165 cached NASA cases, historical timezone transitions, raw cusp boundaries, finite-difference speeds, fallback rejection, asset integrity, unsupported dates and exact JSON round trips.
- The original 87 research checks passed separately and remain unchanged (`evidence/research-87.xml`). They are not counted as new astronomical validation.
- Six frontend geometry tests passed, including a 72-object dense-label stress case, unrounded markers, orientation, and display carry boundaries. The TypeScript check and production frontend build passed.
- A real protected Vercel function returned all 72 enabled objects. Its Linux/Python 3.12.14 longitudes equal the local Windows/Python 3.11.9 results exactly; every direct ephemeris calculation returned flags 258 (`evidence/cloud-local-comparison.json`).
- The same double-precision coordinate record feeds the wheel marker, position table, inspector and JSON export. Label collision avoidance changes text placement with connecting leaders; it does not change the astronomical marker. Display precision is a formatting choice only.
- Actual browser JSON and SVG downloads both contained 72 objects with zero longitude difference from the calculation response. Switching to Basic and importing the JSON restored 72 wheel markers and 72 table rows with zero raw-coordinate mismatches (`evidence/browser-export-validation.json`). REA desktop and 390-pixel mobile workflows completed without captured page errors; screenshots and structured captures are retained in `evidence/rea-chart-*` and `evidence/chart-*.png`.

## Capability and release boundaries

The current catalog contains 74 entries, of which 72 are enabled. Two Sophia variants remain disabled because their procedures have not been sufficiently verified. Spark, directional aspects, progressions, and other unresolved procedures are not invented. Extended chart types, arbitrary asteroid discovery and range ephemerides are not complete features of this v0.1 implementation.

Supabase account/saved-chart UI and the ownership-protected migration are implemented. Application of the migration and live storage verification require access to the designated project; until recorded otherwise, cloud persistence is not claimed verified.

Vercel deployments remain authenticated. Public activation requires the Swiss Ephemeris licensing choice described in the [official vendor terms](https://www.astro.com/swisseph/swedownload_e.htm): the applicable AGPL-compatible route or a professional license. This repository does not establish that a professional license has been purchased.

Reference conventions: [NASA Horizons manual](https://ssd.jpl.nasa.gov/horizons/manual.html), [Swiss programmer documentation](https://www.astro.com/swisseph/swephprg.htm). Raw queries, responses and residuals remain in the repository for review.
