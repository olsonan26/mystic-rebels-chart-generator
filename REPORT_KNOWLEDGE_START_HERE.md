# Read the saved meanings and report sources

Use repository **olsonan26/mystic-rebels-chart-generator**, branch **codex/phsr-numerology-integration-20261028**. The default `main` snapshot predates this knowledge audit. A default-branch-only search will miss later meanings, source reconciliation and chatbot integration. The earlier methodology branch remains a historical checkpoint.

Open [the knowledge branch](https://github.com/olsonan26/mystic-rebels-chart-generator/tree/codex/phsr-numerology-integration-20261028) and configure your connector or clone to use that exact ref. Do not merge the engineering branch into `main` merely to make an indexer see the data; that can also change the deployed application.

The saved knowledge currently includes **131 concepts, 275 selected assertions, 207 report requirements, 50 findings, 44 capabilities and 30 worked examples**. There are **730 targeted original-image reviews and299 pending images**. Meanings and vocabulary are present. Source completeness, numerical validation and full report implementation remain unfinished; **all 18 report sections remain unready**. Seven requirements now carry explicit partial component evidence for the [receiving-context increment](docs/research-20261029/DIRECTED_CONTEXT_IMPLEMENTATION.md); their full dispositions remain unchanged. Packaging these records does not make their claims empirically validated or approve personal reports.

## Use the source meanings for signs, Chiron and Eunomia

**Do not leave these topics to an existing library.** [source_meaning_profiles.json](data/knowledge/source_meaning_profiles.json) now contains all12 original sign core entries, Chiron's reviewed Fractured Structures vocabulary and both Eunomia alternatives. See [REPORT_COMPONENT_USE.md](docs/REPORT_COMPONENT_USE.md) for the exact replacement instruction and working consumer.

There are60 supported vocabulary annotations and one explicit conflicting-alternatives output. Chiron's source-vocabulary support is separate from the aggregate example/orbit gaps. Original686 is present; the compilation's missing-page note is historical. Eunomia is shown with both source definitions, with no silent winner or generic substitution. `external_library_fallback_allowed=false` applies throughout the consumer contract.

## Pull these files

For ingestion, read [the machine manifest](data/knowledge/report_knowledge_manifest.json), then its seven topic packets for bounded connector reads. [The complete audit-text bundle](data/knowledge/report_knowledge_bundle.json) is a roughly9.2 MB bulk-download alternative; exact sizes/hashes are in the manifest. Topic packets include transitive context, matching assertions and findings, and requirement references; use the canonical requirement authority for full required facts and gates. The bulk bundle includes unchanged copies of eleven canonical JSON authorities, including all609 image-bound annotations, both original-review logs and the relationship component profile. Exact source IDs, hashes, conflicting findings, limitations and approval flags stay attached. `--check` rejects stale exports after canonical records change. Authority hashes declare UTF8_UNIVERSAL_NEWLINES normalization so Windows/Linux Git checkouts produce identical exports; original witness image/OCR hashes are retained exactly.

For direct ingestion, use these canonical files:

| Need | File and fields |
|---|---|
| Meanings, vocabulary, sign/decan/degree context and exceptions | [interpretive_inventory.json](data/knowledge/interpretive_inventory.json): `records[].meaning_summary`, `exceptions`, `requires_concepts`, `witnesses`, `line_reconciliation_finding_ids`, `answer_use`; also `report_sections` |
| Original-source propositions and applicability | [original_assertions.json](data/knowledge/original_assertions.json): `assertions[].proposition`, `applicability`, `exclusions_and_limits`, `requires_concepts`, `witnesses`, execution/answer restrictions |
| Every report section, required fact and dependency | [material_requirements.json](data/knowledge/material_requirements.json): `sections`, `requirements`, chart-fact requirements, dispositions and personal-answer gates |
| Contradictions, missing rules and limits | [source_blocker_findings.json](data/knowledge/source_blocker_findings.json): every matching `concept_ids` finding, linked assertion/annotation IDs and remaining questions |
| Checked passages and original-review context | [source_line_annotations.json](data/knowledge/source_line_annotations.json), [source_review_updates.json](data/knowledge/source_review_updates.json), [source_review_continuation.json](data/knowledge/source_review_continuation.json) |
| Calculation availability and source examples | [capabilities.json](data/knowledge/capabilities.json), [worked_examples.json](data/knowledge/worked_examples.json) |
| Bounded directed reach and receiving structure | [relationship_rule_profiles.json](data/knowledge/relationship_rule_profiles.json): numeric parameter evidence, conjunction/receiver contracts, explicit unimplemented scope and partial requirement progress; full-method approval remains false |

For all retained engineering, audit and release history, read [PROFILE_REPORT_KNOWLEDGE_PATH.md](docs/PROFILE_REPORT_KNOWLEDGE_PATH.md). Older summaries preserve historical counts; the manifest and current canonical JSON provide the present export snapshot. Regenerate the export after each source-audit update.

## Find the right topic

| Topic | Concept IDs / retrieval route |
|---|---|
| Sun through Pluto | `meaning-sun` through `meaning-pluto`, plus `planet-lexicon` and `planet-categories` |
| Twelve houses | `house-field`, `field-01` through `field-12`; preserve natural Field versus actual sign |
| Signs, degrees and decans | `tone-pulse`, `spark-entry`, `phsr`, and applicable original assertions/reviews; the12 core sign entries are in source_meaning_profiles.json; full contextual synthesis remains separate |
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

The original images, compiled PDF, OCR and SQLite indexes remain private/local and are excluded from Git. GitHub readers receive reviewed summaries and citation metadata. A new clone cannot run private-source witness retrieval until those assets are restored and their hashes verified. Requirement code fingerprints explicitly trace the committed HEAD tree (or the included files in a Git-less source archive), excluding unrelated local worktree fixes. They still detect changes to the published code; this is provenance rather than personal-report approval. On the source workstation, `python scripts/knowledge_audit.py concept meaning-sun --section profile-foundation` retrieves the fuller witness packet; that command depends on the local source index.

Rebuild/check the portable export from the repository root:

```sh
python scripts/export_report_knowledge.py
python scripts/export_report_knowledge.py --check
```

Copy this instruction to a repository-reading assistant:

> Read olsonan26/mystic-rebels-chart-generator at ref codex/phsr-numerology-integration-20261028, not the default main snapshot. Start with REPORT_KNOWLEDGE_START_HERE.md and data/knowledge/report_knowledge_manifest.json, then use its component_use catalog and relevant topic_packets; the bulk bundle is optional. Use eligible chart vocabulary annotations and relationship components within their actual scope without treating them as validated personal claims or a complete method. Preserve all source restrictions, dependencies, exceptions, competing witnesses and unready report gates. Report what meanings and partial runtime components exist and what remains incomplete. Do not conclude that meanings are absent from a main-only search, and do not treat stored source vocabulary as approval to generate personal conclusions.
