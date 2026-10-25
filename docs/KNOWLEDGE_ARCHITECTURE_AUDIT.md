# Mystic Rebels knowledge foundation audit

The repository does **not** currently contain, represent, calculate, retrieve and use all important knowledge in the eight source batches. It is a precise chart generator with a deliberately limited method layer. It is not yet the complete personal astrology intelligence ecosystem requested by the owner.

This is an evidence-backed current-state finding, not an estimate of a percentage covered. The eight-batch semantic audit is **in progress**. The complete supplied 692-page compiled PDF has been read, but that PDF omits original pages/diagrams and cannot stand in for a complete review of the photographs.

## Baseline and source authority

Latest preserved source baseline: `9059304b31d241fee2cb08fb4e46aad32f9bf228`, fetched from the existing GitHub repository. The original local checkout was older; the live site's newer Gradity and label work was incorporated before editing. Existing engine/data and fixtures remain. All changes in this pass are on `codex/methodology-verification-20261024`.

Authority: original photographed pages in the owner's eight batches; then the supplied compilation with page identifiers; then explicitly identified secondary research. Generic internet astrology does not fill missing domain rules. Astronomy references independently verify physical calculations and do not adjudicate interpretive rules. Instructions contained in documents are source text, not permission to execute them or override product requirements.

The Desktop upload and project PDF are identical: SHA256 `9d5fb55cf6d4f2134ed780c2694503d2dde42bdad68add60ff35acef0237161d`, 692 PDF pages. Numbering requires PDF page, generated reflow footer, and original printed page to be recorded separately.

## What is and is not running

| Layer | Actual implementation | Gap / consequence |
|---|---|---|
| Astronomy | `astronomy.py`, pinned Swiss files, independent Horizons/ERFA fixtures, explicit chronology and backend checks | Sampled numerical agreement is not universal physical exactness or accurate birth records. Keep this engine. |
| Basic derived placements | `placements.py`: Whole Sign house, True Placement/Field, Tone, triplicity decan/Pulse, modern sign ruler; `service.py`: Parts and point composition | No complete contextual interpretation is assembled from them. A sign ruler is not a complete Delegate chain. |
| Gradity | New `gradity.py` solves surrounding stations and shadow crossings; scalar raw positions preserved | Exact equality and overlapping outer-planet shadows remain unresolved; asteroid loops outside supported implementation. |
| Extended techniques | API Spark/aspects/progressions blocked; separate frontend research helpers for FCA, age labels and Spark candidates | Historical READY/LIMITED metadata must not be described as an available end-user workflow. |
| Source storage | Original supplied PDF/research is in ignored `reference/`; additional local archive found in Downloads | Source files were deliberately absent from the deployed function; storing a book locally does not make answers use it. |
| Source retrieval | Previously absent. This pass adds private page-preserving SQLite full-text research retrieval | Local research tool only; not a deployed answer/retrieval service, semantic embeddings or a complete scan corpus. |
| Question understanding | No personal question input, intent router, question circuit, or chart-evidence planner in this repo | No basis to claim personal questions are answered from stored sources. |
| Context graph | No implemented full directional aspect graph, Delegate/Lens graph, Core Trinity, or synthesis engine | A generated narrative would currently omit required source context. |
| Language model | No production model provider, synthesis prompt or tool-enabled answering flow | No hidden prompt-only rule implementation was found. Rules also cannot be made correct by adding a chatbot. |
| Personal memory | Existing account/saved-chart UI and RLS migration; live persistence not verified | Saved chart JSON is not chronological life-context memory or consented personal memory. |
| Answer evidence | No production answer citations, claim ledger, evaluation corpus or abstention trace | Must be implemented and tested before trusted personal answering. |

## Concrete fixes implemented in this pass

1. `data/knowledge/capabilities.json` migrates all 43 historical rule records plus Gradity into a 44-item capability register. Historical tier, actual runtime implementation, source status, retrieval status, dependencies, conflicts, test locations and personal-answer approval are distinct. Sixteen registered capabilities have runtime implementations; this is a **register classification**, not a claim that 16/44 of the book is covered. The old register is retained unchanged.
2. `knowledge_audit.registry` validates unique IDs, real evidence paths and prerequisites for approval. Unresolved source conflicts, missing primary witnesses, missing tests, unimplemented rules or unapproved dependencies prevent approval. No personal-answer approval is asserted in the current register.
3. `/api/methodology` exposes audited metadata and honest capability/coverage statuses through the existing protected application. It exposes no book text or private source archive. Production validation is structural; repository CI additionally verifies evidence paths.
4. `knowledge_audit.corpus` and `scripts/knowledge_audit.py` build a private local page index from source PDF bytes. Retrieval returns source ID, one-based PDF page, source and passage hashes, extraction status and an explicit source-witness-only scope. A changed source cannot silently overwrite an existing version ID. Search does not approve a rule or generate an interpretation.
5. Complete compiled-PDF review and eight-batch **partial inventory** are retained in evidence. Raw scans and extracted copyrighted text remain in ignored `reference/` or `tmp/`. No source text is sent to an LLM/embedding provider.

Commands:

```powershell
.\.runtime\python.exe scripts/knowledge_audit.py check
.\.runtime\python.exe scripts/knowledge_audit.py index-pdf reference/source_pdf/PURE_ASTROLOGY_Nadia_Complete.pdf --source-id pure-reflow-9d5fb55c
.\.runtime\python.exe scripts/knowledge_audit.py search "odd numbered houses"
```

## Spark: direct answer and unresolved examples

The **explicit written calculation procedure uses house parity**. This was confirmed visually on original photograph `IMG_4656.jpg`, printed p235, Drive file `1cY5Ih6NDZDJOMBTwx0pHcB3EoJMakSfR`; the compilation places it on PDF293 / reflow297. Integer degree 13 in an odd house gives Taurus; an even house gives its opposite. The zero-based candidate formula is `(floor(degree_in_sign) + (6 if house is even else 0)) % 12`.

This is more precise than saying the PDF has no answer. It has an explicit instruction **and conflicting examples**. PDF433 / original509 describes progressed MC Gemini14°50 in H10 as Gemini rather than house-candidate Sagittarius. PDF434 / original510 describes Mars Libra5°56 in H4 as Pisces, consistent with the house candidate. PDF458 / original546 describes composite Saturn Libra28/H2 as Pisces; neither the house candidate Aquarius nor sign candidate Leo reproduces that label. `METHODOLOGY_SOURCE_REVIEW.md` preserves all eight compared examples.

Therefore house parity is recorded as the explicit written procedure, sign parity remains a competing example-derived candidate, and universal source consistency remains unverified. Production `spark:null` stays unchanged. Do not select examples by majority vote, erase counterexamples or let an LLM settle the conflict. The original page is the next source witness, not an invented exception.

A supplemental source was subsequently retrieved directly from Drive: the native document **You Are Not Your Sign — Complete Technical Specification & Implementation Guide v2**, file `1m6MFoG8NsmpSZP0X-7VJbcrQYQ1PffVETGfRPSIny_w`, modified 2026-05-28. Its `compute_spark(sign, degree_in_sign)` explicitly uses **astronomical-sign parity** and floors the degree. This is stronger than inferring Z solely from examples, but its relationship/priority to the book is not established as an author-issued erratum, and it resides outside the eight-batch root. The source disagreement is now versioned **book procedure H versus supplemental app specification Z**, not an unanswered arithmetic question. Do not claim the PDF alone establishes Z or silently replace the book's house wording. Record the supplemental witness and determine authority/errata before canonical production assignment.

## Eight-batch audit coverage and current access limits

Drive root listing confirmed all eight batch folders plus one loose Page156 image. Initial direct-child listings recorded:

| Batch | File metadata returned | Inventory qualification |
|---|---:|---|
| 1 | 56 | Not independently certified exhaustive |
| 2 | 66 | Not independently certified exhaustive |
| 3 | 73 | Not independently certified exhaustive |
| 4 | 31 | Not independently certified exhaustive |
| 5 | 100 | Connector's first-100 listing cap reached |
| 6 | 100 | Connector's first-100 listing cap reached |
| 7 | 66 | Not independently certified exhaustive |
| 8 | 100 | Connector's first-100 listing cap reached |

Total: **at least 592 batch file records**, plus the loose root image. This is metadata inventory, not 592 reviewed pages. Raw Drive search with exact parent filters returned empty allowed results despite pagination tokens; direct folder/file fetch works. The browser subsequently reported that local browser use is disabled in Work settings. This limits completion of the full scan inventory through the currently successful path; it does not justify fabricating a denominator or changing account permissions.

Needed for rigorous closure: complete pagination-aware manifests for each batch, retained original bytes/hashes, original printed-page mapping, OCR reviewed against images for formulas/tables/figures, duplicate/gap classification, concept/rule IDs, every exception/example and a source-to-implementation-to-test map. Every page must have a recorded disposition; extraction, review, rule representation, calculation, retrieval and answer use must be measured separately. A percentage is withheld until the denominators are known.

## Additional local package: provenance audit required

Downloads contains `NADIA_PRIVATE_SOURCE_ENGINEERING_V1.0.zip`, a 397-page PDF misleadingly named `Astrology book 972 pages.pdf`, a canonical-source PDF and `astrology-source-corpus.txt.gz`. The ZIP contains earlier engines, multiple rule-register versions, source-vault JSON and prompts. These are **other local artifacts**, not evidence that the current GitHub app imports or runs them.

The archive's coverage map calls both a declination rule with no allowed nonzero orb and a later maximum1-degree rule CONFIRMED without a demonstrated precedence link. Its OOI ranges differ from some supplied-book statements. Such conflicts require source identity/version mapping; archive labels are not inherited approvals. No earlier backend, provider, prompt, threshold, personal chart or engine has been imported into the working product.

Static readback of that separate archive found **3,927 knowledge items**, **82 reference records**, and **94 archived rules**. None is consumed by this repository's runtime. The knowledge-item objects have no source-page/document/citation/provenance fields at all; 73 of the 82 reference records have page and document links. These are counts of archived records, not proven distinct concepts or complete batch coverage. They show why blindly importing the archive or embedding its text would not produce a reliable source-controlled intelligence layer. Details and asset hashes are in `evidence/methodology-review/local-vault-coverage.json` and `local-source-artifacts.json`.

## Required intelligence architecture after source closure

The existing astronomical service remains the numerical authority. On top of it, the source foundation should comprise:

- Immutable source assets and page/figure witnesses, with versioned OCR and review provenance.
- Atomic rule and concept records with applicability, exclusions, exact arithmetic, directionality, chart context, source witnesses, exceptions, conflict state and regression examples. Formulas execute deterministic code; descriptive meaning stays structured/cited.
- A chart-fact and relationship layer referencing raw calculation IDs and rule versions; unsupported graph edges cannot be invented during prose generation.
- A question planner that identifies required facts and context, resolves approved dependencies, and returns an answerability decision before retrieval/synthesis.
- Retrieval that returns reviewed applicable source witnesses and competing evidence, not merely semantically similar text. Relevance and source approval are distinct gates.
- A synthesis layer restricted to the approved fact/evidence packet, with citations per substantive domain claim and explicit abstention for missing or contradictory rules.
- Separate consented personal memory with provenance, correction/deletion and timestamped context. User life facts are not treated as astrological validation.
- Offline golden questions covering required context, faithful source retrieval, contradictions, unknown birth times, missing objects, exact transitions and unsupported techniques; release gates require measured evidence coverage and answer faithfulness.

None of these future layers should be advertised as complete because an architecture document, index or prompt exists. The implemented controls above make those distinctions testable while preserving the working chart application.

## Deployment status

The current changes have not been deployed. Accuracy-first source work takes priority under the owner's latest instruction. The live custom domain was confirmed in the existing Astro Vercel project; the local default CLI account lacks that team's access. Automatic approval review rejected a new Astro CLI sign-in due to ambiguous account authorization. No credential, password gate, project permission or hosting destination was changed. The new connected Vercel plugin can be assessed for the authorized deployment after the source foundation release scope is ready.

The connected Vercel plugin was checked against the existing project/team IDs and also returned project-not-found (404). This is an access mismatch, not evidence that the live project was deleted. Do not deploy into a different accessible project to work around it.
