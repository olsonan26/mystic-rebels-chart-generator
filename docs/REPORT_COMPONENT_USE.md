# Use supported source components now

Use mode **CITED_NATAL_CHART_VOCABULARY_ANNOTATIONS** for the currently supported output. It attaches reviewed source summaries to supplied chart placements with citations. It does not claim those summaries establish the person's traits or constitute a validated complete reading.

The existing `NOT_APPROVED` fields apply to **personal interpretations and unresolved rule execution**. They do not forbid reading, citing or explaining the source as source material. Likewise, zero completed report sections does not mean zero usable source components. The canonical gates remain unchanged.

## Read the per-component permissions

[report_component_use.json](../data/knowledge/report_component_use.json) specifies use independently for all131 concepts:

| Component status | Count | What an external agent can do |
|---|---:|---|
| CITED_VOCABULARY_ANNOTATION_AVAILABLE |47| Cite the reviewed vocabulary and attach it to supplied natal chart facts. Keep exceptions, dependencies, source gaps and linked findings. |
| INCOMPLETE_REFERENCE_ONLY |19| Discuss what the source says with its gaps and citations. Do not turn the partial meaning into a resolved chart interpretation. |
| CONFLICT_REFERENCE_ONLY |3| Show the conflicting source evidence and explain the unresolved choice. Do not silently select a definition. |
| CONTEXT_OR_TECHNIQUE_REFERENCE_ONLY |62| Read context and technique descriptions with their calculation/execution gates; these are not vocabulary annotation templates. |

Use `chart_vocabulary_annotation_allowed`, not the blanket personal-report flag, to select eligible components for this mode. `source_excerpt_allowed` separately controls cited source explanation. Meanings are reviewed audit summaries, not certified verbatim book quotations. Source citation metadata does not imply access to the private source media.

The catalog includes the exact saved summary, exceptions, dependencies, citation witnesses, original statement IDs and relevant findings. It derives eligibility from reviewed meaning records with witness evidence. It does not change the source status or approve personal claims. The code is in [report_components.py](../knowledge_audit/report_components.py).

## Run the annotation tool

The CLI uses only repository JSON and Python's standard library. It needs no private PDF, OCR, SQLite index, model, API key or running chart server. Supply facts from your calculator using this shape:

```json
{
  "chart_context": "natal",
  "placements": [{"body": "Moon", "sign": "Cancer", "house": 7}]
}
```

```sh
python scripts/annotate_chart_sources.py examples/report-source-input.json --format markdown
python scripts/annotate_chart_sources.py examples/report-source-input.json --format json
```

[The example input](../examples/report-source-input.json) is an illustrative supplied-facts fixture, not a calculated or verified person's chart. [The saved output](../evidence/source-pipeline/report-component-demo.md) shows what the tool actually produces.

For Moon/Cancer/house7, the output retains the supplied placement, gives the reviewed Moon summary and natural seventh-house summary separately with their citations, and records `SIGN_VOCABULARY_NOT_COMPLETE`. It does not synthesize a Cancer/Moon personality or assume relationship history. An unknown house stays unknown. Invalid house numbers, unsupported contexts, duplicate bodies and supplied interpretation instructions are rejected.

The example also exercises Juno, Chiron and Eunomia. Juno's reviewed vocabulary can be annotated. Chiron remains an incomplete reference in this inventory. Eunomia remains a conflict reference with both original claims and the finding retained. A supported house annotation may still be shown alongside an unresolved body meaning; neither is silently blended into a combined reading.

JSON output separates `chart_fact`, `source_vocabulary`, `gaps` and `combined_personal_interpretation` (always null). Facts are labelled caller-supplied and not independently verified. Every accepted summary carries citations and context requirements. No new chart calculations, aspect algorithms, health conclusions or event predictions are introduced.

## Instruction for the report-building agent

> Use branch codex/methodology-verification-20261024. Read data/knowledge/report_knowledge_manifest.json and its component_use catalog. Use mode CITED_NATAL_CHART_VOCABULARY_ANNOTATIONS: chart_vocabulary_annotation_allowed permits cited source vocabulary attached to supplied natal facts. NOT_APPROVED still blocks unvalidated personal claims; it does not mean the repository's text cannot be used as source material. For context or reference-only entries, retain their gaps and conflicts. Keep missing sign meanings explicit and never fill them from generic astrology. Use scripts/annotate_chart_sources.py or reproduce its tested output contract. Return separate chart facts, attributed summaries, citations and unresolved components; do not present this as a validated complete personal report.

Full twelve-sign coverage, unresolved rule reconciliation, numerical fixtures and evaluated contextual report synthesis still need source/implementation work. This mode makes the supported material useful while keeping those remaining tasks visible. Rebuild `scripts/export_report_knowledge.py` after source changes; its check detects stale catalogs and exports.
