# Mystic Rebels implementation

Product: independent Mystic Rebels professional astrology chart generator. Local Python API and React/TypeScript client; no Astro.com runtime dependencies.

The supplied historical research files remain unchanged and private in `reference/`. Product identity is Mystic Rebels. Public-facing copy avoids research terminology. Calculation details remain available on demand.

## Design direction

Observed on https://mysticrebels.com/ on 2026-10-24: Montserrat typography, purple navigation/backgrounds, bright magenta pill buttons (#c500ff), white text, cyan logo accents. Adapt these to a focused chart workspace: violet header, readable light chart canvas, deep plum surrounding controls, magenta primary action, cyan selection marks. The large accurate chart is the focal point; no decorative stars or generic marketing hero.

Core palette: plum #39064e, violet #70158b, magenta #c500ff, cyan #20e3e6, white #ffffff, ink #24142f. Montserrat is used throughout with tabular numeric tables. Desktop: birth/object controls left, chart and results right. Mobile: stacked birth details, chart, selection and positions.

## Release gates

- Official file assets with origin, retrieval time and SHA256.
- Per-object requested/returned backend flags; fail on silent fallback.
- Separate independent astronomical QA and unchanged historical research checks.
- Runtime capability gates for unsupported rules and objects.
- Single full-precision point record shared by wheel, table, inspection, export.
- Private source book excluded from release/build/static serving.
- Before public service activation, select an appropriate Swiss Ephemeris license per vendor terms. The hosted development application remains authenticated while this release gate is unresolved.
