# Read the saved meanings and report sources

Use repository **olsonan26/mystic-rebels-chart-generator**, branch **codex/methodology-verification-20261024**. The default `main` snapshot has 227 files and one commit; it predates this knowledge audit. A default-branch-only search will miss the saved meanings. GitHub has four branches as verified on 25 October 2026.

Open [the knowledge branch](https://github.com/olsonan26/mystic-rebels-chart-generator/tree/codex/methodology-verification-20261024) and configure your connector or clone to use that exact ref. Do not merge the engineering branch into `main` merely to make an indexer see the data; that can also change the deployed application.

The saved knowledge currently includes **131 concepts, 250 selected assertions, 207 report requirements, 49 findings, 44 capabilities and 30 worked examples**. Meanings and vocabulary are present. Source completeness, numerical validation and report implementation remain unfinished; **all 18 report sections remain unready**. Packaging these records does not make their claims empirically validated or approve personal reports.

## Pull these files

For ingestion, read [the machine manifest](data/knowledge/report_knowledge_manifest.json), then its seven topic packets (each under 600 KB) for bounded connector reads. [The complete audit-text bundle](data/knowledge/report_knowledge_bundle.json) is an 8.6 MB bulk-download alternative. Topic packets include transitive context, matching assertions and findings, and requirement references; use the canonical requirement authority for full required facts and gates. The bulk bundle includes unchanged copies of nine canonical JSON authorities, including all 589 image-bound annotations and both original-review logs. Exact source IDs, hashes, conflicting findings, limitations and approval flags stay attached. `--check` rejects stale exports after canonical records change. Authority hashes declare UTF8_UNIVERSAL_NEWLINES normalization so Windows/Linux Git checkouts produce identical exports; original witness image/OCR hashes are retained exactly.

For direct ingestion, use these canonical files:

| Need | File and fields |
|---|---|
| Meanings, vocabulary, sign/decan/degree context and exceptions | [interpretive_inventory.json](data/knowledge/interpretive_inventory.json): `records[].meaning_summary`, `exceptions`, `requires_concepts`, `witnesses`, `line_reconciliation_finding_ids`, `answer_use`; also `report_sections` |
| Original-source propositions and applicability | [original_assertions.json](data/knowledge/original_assertions.json): `assertions[].proposition`, `applicability`, `exclusions_and_limits`, `requires_concepts`, `witnesses`, execution/answer restrictions |
| Every report section, required fact and dependency | [material_requirements.json](data/knowledge/material_requirements.json): `sections`, `requirements`, chart-fact requirements, dispositions and personal-answer gates |
| Contradictions, missing rules and limits | [source_blocker_findings.json](data/knowledge/source_blocker_findings.json): every matching `concept_ids` finding, linked assertion/annotation IDs and remaining questions |
| Checked passages and original-review context | [source_line_annotations.json](data/knowledge/source_line_annotations.json), [source_review_updates.json](data/knowledge/source_review_updates.json), [source_review_continuation.json](data/knowledge/source_review_continuation.json) |
| Calculation availability and source examples | [capabilities.json](data/knowledge/capabilities.json), [worked_examples.json](data/knowledge/worked_examples.json) |

For all retained engineering, audit and release history, read [PROFILE_REPORT_KNOWLEDGE_PATH.md](docs/PROFILE_REPORT_KNOWLEDGE_PATH.md). Older summaries preserve historical counts; the manifest and current canonical JSON provide the present export snapshot. Regenerate the export after each source-audit update.

## Find the right topic

| Topic | Concept IDs / retrieval route |
|---|---|
| Sun through Pluto | `meaning-sun` through `meaning-pluto`, plus `planet-lexicon` and `planet-categories` |
| Twelve houses | `house-field`, `field-01` through `field-12`; preserve natural Field versus actual sign |
| Signs, degrees and decans | `tone-pulse`, `spark-entry`, `phsr`, and applicable original assertions/reviews; this is not a claim of a complete approved twelve-sign dictionary |
| Cusps and blending | `fringe-fca`, `anchors`, linked width/exception conflicts |
| Aspect meanings | `spectrum-meanings`, `directional-context`, `vantage-resolution`, `handoff`, `forced-contact`, `block-color`, `free-theory`, `clusters` |
| Asteroids | `chiron`, all `asteroid-*` records and their original assertions; preserve contradictory definitions such as Eunomia |
| Report assembly | `objective-context`, `agency`, `phsr`, `core-trinity`, `delegate-condition`, and the chosen report section's transitive dependencies |

Example: `meaning-sun` retains “Vitality, existence, personal expression, play, purpose and children.” `meaning-jupiter` retains expansion, experience, exploration, beliefs and teaching, while `planet-lexicon` warns that Jupiter alone does not mean money. These are source summaries with contextual limits, not ready-made conclusions about an individual.

## Keep the evidence attached

1. Verify repository, branch and manifest before searching. An export missing its exceptions, conflict records or approval flags is incomplete.
2. Load the chosen report section, its concepts and transitive dependencies, required chart facts and applicable source assertions. Interpret sign, house, degree/decan, aspect direction, ruler condition and chart layer in their stated contexts.
3. Keep every relevant conflicting witness and the stated limitations. Do not infer user history, diagnose health, guarantee events or replace a missing rule with generic astrology. `NOT_APPROVED` and `NOT_READY_FOR_PERSONAL_REPORT` must remain effective gates.
4. Cite original file ID, image hash, printed header and annotation line range where available. Keep compiled-PDF page witnesses separate from original-image evidence. Metadata does not mean the reader has independently seen the source media.
5. Separate source fidelity, astronomical calculation checks, contextual synthesis and empirical outcome validation. The first two alone do not certify accurate personal reports. Build and evaluate the missing report/context layer before enabling it.

The original images, compiled PDF, OCR and SQLite indexes remain private/local and are excluded from Git. GitHub readers receive reviewed summaries and citation metadata. A new clone cannot run private-source witness retrieval until those assets are restored and their hashes verified. On the source workstation, `python scripts/knowledge_audit.py concept meaning-sun --section profile-foundation` retrieves the fuller witness packet; that command depends on the local source index.

Rebuild/check the portable export from the repository root:

```sh
python scripts/export_report_knowledge.py
python scripts/export_report_knowledge.py --check
```

Copy this instruction to a repository-reading assistant:

> Read olsonan26/mystic-rebels-chart-generator at ref codex/methodology-verification-20261024, not the default main snapshot. Start with REPORT_KNOWLEDGE_START_HERE.md and data/knowledge/report_knowledge_manifest.json, then ingest the relevant topic_packets listed in that manifest; the bulk bundle is optional. Preserve all source restrictions, dependencies, exceptions, competing witnesses and unready report gates. Report what meanings exist, what is incomplete and what runtime/report integration is still absent. Do not conclude that meanings are absent from a main-only search, and do not treat stored source vocabulary as approval to generate personal conclusions.
