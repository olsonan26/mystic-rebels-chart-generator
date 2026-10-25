# Use the audited meanings instead of an existing library

Use branch `codex/methodology-verification-20261024`. The current source profiles replace generic-library meanings for all twelve sign core entries and Chiron. Eunomia is included as two unresolved creator-authored alternatives. **Do not leave these topics to an existing library, omit them silently, or substitute a generic interpretation when source evidence has a gap.**

The source-backed annotation mode now offers **60 vocabulary components**: the previous47, Chiron's scoped core meaning and all12 sign entries. One additional component, Eunomia, offers cited alternatives without selecting either. The143 consumer components consist of131 existing thematic concepts plus12 sign cards; this does not change the131-record thematic denominator or approve a complete personal report.

## What changed

| Topic | Source-grounded behavior |
|---|---|
| Chiron | Originals683,685-686 and770 support Fractured Structures: comparison with established standards, ill-fitting structures, insecurity around not fitting, and developing an individual, inventive way. The automatic Wounded Healer substitution is explicitly rejected. Original686 exists; its missing-page note belongs to the compiled PDF. |
| Chiron's unresolved examples | Jackson's Saturn sextile/trine disagreement and orbit/date wording remain linked, but they do not erase the independently supported core vocabulary. No numerical or clinical rule is approved. |
| All twelve signs | Original197 sets the expression-style scope;198-202 directly describes all twelve signs. Original185-186 gives the modern rulers;203-205 distinguishes shared Mercury/Venus themes and the separate orbital-position layer. These are direct source summaries, not a dictionary borrowed from another system. |
| Eunomia | The output shows both dedicated-chapter Refined Resilience (711-712) and comparative-table Functional Order (772), with the unresolved conflict visible. It selects neither and does not merge them. |
| Other partial entries | Their source references and citations remain visible with limitations. Missing evidence produces an explicit gap, never an existing-library fallback. |

The narrow sign core-coverage gap is closed. Exhaustive sign/aspect/ruler synthesis and full personal-report validation remain unfinished. Source vocabulary, user traits and empirically validated outcomes remain different claims.

## Files and machine permissions

Read [source_meaning_profiles.json](../data/knowledge/source_meaning_profiles.json) first for the14 compact, reviewed profiles:12 signs, Chiron and Eunomia alternatives. Each has original file ID, image/OCR hashes, inspected printed page, exact OCR locator ranges and linked review annotations. Physical media remain private; these are reviewed summaries with citation metadata.

Then read [report_component_use.json](../data/knowledge/report_component_use.json) and [the ingestion manifest](../data/knowledge/report_knowledge_manifest.json). The catalog separates `chart_vocabulary_annotation_allowed`, `chart_alternatives_annotation_allowed`, `source_excerpt_allowed`, and personal-report approval. All records explicitly prohibit external-library fallback. Relevant topic packets also include the reviewed profiles.

The canonical Chiron aggregate status remains incomplete because example/numerical questions remain. Its separate reviewed-vocabulary profile permits the supported definition. Do not use the aggregate status to drop that definition. For Eunomia, do not use the conflict status to drop both alternatives.

## Run the working consumer

The CLI uses repository JSON and Python's standard library. It requires no model, API key, private PDF/OCR/index, or running chart server:

```sh
python scripts/annotate_chart_sources.py examples/report-source-input.json --format markdown
python scripts/annotate_chart_sources.py examples/report-source-input.json --format json
```

[The illustrative input](../examples/report-source-input.json) supplies Moon/Cancer/H7, Juno/Taurus/H10, Chiron/Aries/H5 and Eunomia/Virgo/H4. These are demonstration facts, not a verified person's chart. [The saved Markdown](../evidence/source-pipeline/meaning-repair-demo.md) and [JSON output](../evidence/source-pipeline/meaning-repair-demo.json) show the current behavior.

Output separates supplied `chart_fact`, supported `source_vocabulary` (body, house and sign), `source_alternatives`, partial `source_references` and explicit `gaps`. It retains citations, context requirements and held-out findings. It does not claim to have independently checked the supplied positions or generated a validated personal reading. Unknown houses remain unknown and invalid inputs are rejected.

## Paste this to the other agent

> Refresh branch codex/methodology-verification-20261024. Read data/knowledge/source_meaning_profiles.json and data/knowledge/report_component_use.json. Replace your existing-library meanings for all twelve sign core entries and Chiron with these reviewed source profiles. Chiron's supported Fractured Structures vocabulary must be included; its example/orbit disagreements are separate held-out claims. Include both Eunomia source alternatives with citations and no selected winner. Do not leave signs, Chiron or Eunomia to your existing library. Honor external_library_fallback_allowed=false: show explicit source limitations rather than silently substituting generic meanings. Use scripts/annotate_chart_sources.py as the tested reference consumer, retaining separate chart facts, source summaries, source alternatives, citations and contextual limits. Full personal-report approval remains separate.
