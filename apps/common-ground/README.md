# Common Ground — local natal comparison prototype

This separate prototype combines preserved name/date numerology calculations with the installed Mystic Rebels natal engine. It adds a transparent, deterministic comparison layer for motivation, communication and work style. It does not modify or deploy either original application.

## Ordered assessment and annual integration

The local app now includes trust/boundaries, voice/emotional needs, autonomy/worth and yearly-direction topics. Each research result contains the seven ordered stages, every assessed ruler, explicit cycle references, separate Delegate occupants and source witnesses. Degree/Spark conflicts and the incomplete directed aspect stage remain visible. No full-method forecast is generated.

Annual ESS/PY/COM and optional monthly outputs use the hash-pinned STAFFprofiler adapter at4172789db1034072f50c78178187e839fa710fb5. Its annual method remains separate from the original LOOKS-LIKE-COSTAR natal method. January1 is the annual boundary. The supplied birth name is used as an explicitly labeled scenario; current-name transitions remain unresolved. The original adult meaning bank is available as reference, with its category and authentic raw-value selection retained.

Select a topic and calendar year after calculating. The JSON export and saved HTML reading include the selected assessment; browser print includes the visible research result. User details remain local unless you explicitly export. The app does not load the published Nadia history into readings.

From this repository, the Windows launcher uses the root `.runtime/python.exe`. With a normal Python environment, install the repository requirements and run `python apps/common-ground/app.py`. Node.js must be on PATH (or set COMMON_GROUND_NODE to its executable) for annual calculations. The root ephemeris/location assets must be provisioned as described by the root README. The source-pack generators require the local source snapshots; the committed generated packs work without those snapshots.

Focused checks: `python -m unittest discover -s apps/common-ground -p "test*.py"`. Browser verification checked Nadia2011 values, the ruler cycle, topic changes, HTML/JSON export, print and390px layout. The first implementation passed37 targeted/regression tests.

## Open it

From this folder, run `launch.ps1` in PowerShell. The installed Mystic runtime is reused; there are no new package installations or cloud API keys.

Open [the local prototype](http://127.0.0.1:8766/). Keep the local server running while using the form. To stop the foreground server, press Ctrl+C in its terminal.

The birth-name and birth details are entered in the form. Choose a matching city result, then create the comparison. The fictional example is labeled as such. User-supplied personal details are not hardcoded in the source or retained server-side.

## What works

- Live city lookup with coordinates and an IANA time zone; supplied coordinate overrides resolve their time zone through the local polygon lookup.
- Actual natal positions from the existing Mystic Rebels Swiss Ephemeris engine.
- Separate Expression, Soul Urge, Birth Force, Ultimate Goal, Balance and Called Name calculations.
- Literal PMEI letter counts, with zero counts preserved.
- Three comparison topics with inspectable source ingredients and questions.
- Editable inputs, unknown/approximate time handling, and explicit DST occurrence selection when required.
- A standalone HTML reading, browser print/PDF, and a user-triggered JSON export.

The app binds only to 127.0.0.1. It does not send chart/name inputs to an AI provider, load the original app's secret files, or save profiles in a database or browser storage. Export files contain the person's details and are created only through the export action.

## Explicit method choices

The natal numerology adapter follows the inspected LOOKS-LIKE-COSTAR core calculator:

- A–Z Pythagorean letter values.
- A/E/I/O/U vowels; Y remains a consonant in this selected method.
- Master values 11, 22 and 33 are preserved in calculations.
- Where the selected meaning bank has no separate master vocabulary, root vocabulary is identified explicitly rather than changing the displayed calculation.
- Ultimate Goal includes both name and date. It is not renamed to a date-only Life Path.
- Called Name uses reduced first name plus reduced last name under that particular source method.
- Full-name Expression, Soul Urge and PMEI retain all supplied name parts.

Other legacy modules differ. Those differences remain documented rather than being silently merged.

The astrology adapter preserves separate house/Field, Tone and Pulse layers. Unknown time uses a clearly labeled noon reference and withholds house/angle-based comparison. Approximate inputs retain their stated uncertainty; this first version does not calculate a complete uncertainty envelope.

## Sources and comparison status

The frozen ingredient pack records GitHub commit identities and original-source witnesses:

- Mystic Rebels audited branch at `3d83db75c30b26d9b068576d84ec49554822fd8c`.
- LOOKS-LIKE-COSTAR at `023140de4ac9ebad8a804b4c984337135e77b19a`.

Definitions come from those sources. Cross-system connections are new analytical proposals. They are not established number–planet rules or empirical correlations. Every natal chart contains the planets; the prototype does not count a planet's existence as confirmation.

The 0/18 personal-report readiness state remains unchanged. This is a research comparison of attributed components; it does not claim to implement a full approved PURE personal report, complete Delegate graph, aspects, Spark, progressions, daily numerology or forecasting.

## Location detail

The installed city list does not include every small city. Los Alamitos, California has a separately attributed prototype-only fallback from the [U.S. Census Bureau BAS26 incorporated-place table](https://tigerweb.geo.census.gov/tigerwebmain/Files/bas26/tigerweb_bas26_incplace_ca.html), GEOID 0643224, CENTLAT 33.7971040 and CENTLON -118.0591800. These are municipal centroid coordinates, not a certified birth-address location. The coordinate basis is retained in each result. The original city dataset is unchanged.

## Files

- `app.py`: local API and static-file server.
- `numerology.py`: explicit natal numerology adapter.
- `compare.py`: deterministic contextual comparison.
- `sources.py`, `data/source-pack.json`: frozen attributed definitions.
- `build_source_pack.py`: reproducible source extraction.
- `static/`: dependency-free browser interface.
- `test_backend.py`, `tests_comparison.py`: targeted verification.

See [the earlier integration analysis](../../reports/mystic-costar-analysis-20261027/COMBINED_ANALYSIS.md) for the fuller source review and unresolved integration questions.

