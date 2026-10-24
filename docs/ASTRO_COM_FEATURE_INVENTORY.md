# Mystic Rebels chart workflow inventory

Inspected on 2026-10-24 with CUA and REA. This is interface research, not a runtime dependency or a copy of proprietary code.

REA public-page evidence: `ev_92d536b57716fb468133cd05d6380d42b3c32cb5fc720f5747599a3db319cc53`, retained in `evidence/rea-astro-reference.json`. The initial ambiguous-selector attempt is retained separately as incomplete evidence.

## Live behavior observed

Birth entry has separate name, date, clock-time and country/town controls. Unknown time is a separate clock choice. Typing a town produces disambiguated locations with coordinates. Greenwich produced 21 choices; selecting Greenwich, England resolved 51°28′37″ N, 0° longitude. Incomplete me/not-me input produced a validation error. Extended settings expose automatic timezone or explicit fixed/local-time choices. The entry requires registration before the complete chart-selection screen, so authenticated extended-control behavior was not observed in this run. No account was created. The user-supplied screenshots provide the remaining control inventory; their effects are not claimed runtime verified.

## Applicable controls and implementation

| Reference control | Mystic Rebels behavior |
| --- | --- |
| Birth date/time and unknown time | Validated local date/time, seconds, stated accuracy, explicit uncertain-time mode |
| Town search / disambiguation | Offline city search with coordinates, IANA zone, editable exact coordinates |
| Automatic time-zone handling | Pinned IANA historical offsets, typed folds/gaps; coordinate-zone lookup |
| Chart type | Natal and Dual views; no invented progressed/relocated procedures |
| House/zodiac/center selectors | Fixed to the required Whole Sign, tropical, geocentric configuration |
| Object multi-select | Search, grouped checkboxes, Basic/Expanded/Custom and all-available selection |
| Mean/true/descending nodes | Separate mean/true nodes; corresponding opposite descending points |
| Lilith variants | Mean and osculating apogee independently computed; unavailable variants clearly disabled |
| Asteroid lists / manual entries | Versioned source-approved numbered catalog, official per-object assets; provisioner supports expansion |
| Aspect/orb controls | Advanced rules remain disabled; no conventional aspect lines substituted |
| Image size / drawing controls | SVG zoom, fullscreen, precision controls, connected labels and object inspector |
| Chart wheel | Raw astronomical markers, independent angles, Whole Sign divisions and distinct energy track |
| Additional tables | Exact position table, raw metadata, JSON/SVG export and browser print |
| Save/default profile | Supabase sign-in and user-owned saved charts, subject to schema provisioning |

Range ephemerides, progressed/relocated overlays, and advanced directional aspect controls remain future modules. The initial release does not present them as finished features.
