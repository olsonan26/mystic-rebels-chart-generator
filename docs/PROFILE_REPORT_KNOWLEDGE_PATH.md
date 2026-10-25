# How the saved audit supports future profile reports

The audit is building a reusable, source-bound knowledge layer for profile reports. It does not yet generate approved personal reports. Source acquisition, OCR, targeted visual review, semantic reconciliation, calculation validation, retrieval and personal answer approval are tracked separately.

| Report-building need | Durable authority | What it preserves |
|---|---|---|
| Source identity and provenance | `data/knowledge/source_manifest.json`, `source_pipeline.json`, `original_page_map.json` | Exact provider file IDs, image/OCR hashes, acquisition stages, inspected headers and candidate PDF mappings |
| Source-specific meanings and exceptions | `data/knowledge/interpretive_inventory.json` | 131 concept records with meanings, applicability/exception context, dependencies and original/compiled witnesses |
| Selected atomic claims | `data/knowledge/original_assertions.json` | Precise propositions, source IDs/hashes, applicability, exclusions, concept dependencies and explicit execution/answer restrictions |
| Image-checked passages and diagrams | `data/knowledge/source_line_annotations.json`, `source_line_reconciliation.json` | Exact image/OCR identity, printed header, selected OCR locator ranges and findings; unchecked lines remain explicit |
| Contradictions and incomplete rules | `data/knowledge/source_blocker_findings.json` | Competing branches, linked assertions/annotations and remaining questions; no silent selection of a preferred witness |
| Worked examples | `data/knowledge/worked_examples.json` plus selected original assertions and annotations | Example-specific context and limits; examples do not automatically become universal rules |
| Profile section requirements | `data/knowledge/material_requirements.json`, `docs/MATERIAL_CONTEXT_RECONCILIATION.md` | 207 atomic requirements across 18 report sections, with source witnesses, implementation gaps, dependencies and dispositions |
| Retrieval proof | `knowledge_audit/semantics.py`, `requirements.py`, `evidence/source-continuation/retrieval-check.json` | Local concept/requirement packets retaining original and compiled counterevidence without generating a personal answer |
| Reproducible updates | `source_review_batch_notes.tsv`, `source_assertion_additions.tsv` and the documented builder sequence | Authored declarations regenerate the saved knowledge instead of relying on chat history |

Original photographs, full candidate OCR and local SQLite indexes are retained privately under the ignored `reference/` directory. Public Git history contains audit declarations, reviewed summaries, provenance, requirements, queues and validation evidence. It intentionally excludes private originals/OCR and credentials. A fresh checkout alone therefore does not contain every photograph or full private transcript: those assets must be restored from the retained private collection or the source provider and verified against their recorded hashes. Git publication is not proof of an independently verified backup of that private collection.

The 25 October presence check confirms all 1,029 acquired original-image files, all 1,028 successful OCR files and both local indexes are present. All 198 selected assertions retain original witnesses and remain unapproved for personal answers. The machine-readable snapshot is `evidence/source-pipeline/profile-report-knowledge-readiness.json`; it records hashes for the knowledge authorities and explicitly distinguishes local retention from independent backup.

## What still separates this knowledge layer from reports

1. Finish source and passage reconciliation, preserving unknowns and conflicting author rules. Having acquired an image does not mean all its content has been semantically reviewed.
2. Verify executable calculations independently: time, observer/frame, motion, wrap, exactness, point emission and technique-specific boundaries. Source fidelity and astronomical correctness are different checks.
3. Connect each report section to actual natal, relocated, transit or relationship chart facts through an explicit context graph. Retain the chart type, epoch, location, body/point, house, ruler chain, directed aspect, motion and relevant conditions for every selected claim. Do not substitute keyword lists for the combined context the source requires.
4. Retrieve the applicable claims and all linked counterevidence, then produce cited, bounded prose that distinguishes author interpretation, calculated fact and user-provided life context. No unsupported personal history, diagnosis, nationality stereotype or guaranteed outcome should be inferred from an anecdote.
5. Evaluate report output with source-fidelity, calculation, applicability, contradiction, citation and full-workflow checks before approving personal use.

All 18 report sections currently remain unready. The saved files support continuing this work and later implementing reports without starting the knowledge audit over; they are not a claim that everything is reconciled or that a report engine already exists. Runtime approval flags and report-readiness gates must remain intact during auditing.

## Locational batch: concrete examples of retained report context

- Printed 790-791: Delegate condition, full relocated chart, natal assessment and the person's purpose for moving precede line interpretation.
- Printed 796-797 and 805: HR/HS/AP/SA sky roles differ from zodiacal AC/DC/MC/IC contacts; signs, houses and rulers still shape expression after chart assessment.
- Printed 808 and 812: natal Paran imprint is retained separately from the new location's added Parans; selection epoch and event-window ambiguity remain open.
- Printed 813: Capricorn Field → Aries Tone → ruler Mars → Cancer Field/Libra Tone → Apex role is retained as a worked context chain.
- Printed 817: the Visibility Spectrum is explicitly unproven research; no operational rule is inferred from it.
- Printed 828-835: Local Space origin, true-north azimuth, direction, output/receipt and physical-travel scope are retained; natal imprint is not overwritten when a new origin is calculated.

These examples are audit-only. See the current continuation report and generated queues for the remaining source work.
