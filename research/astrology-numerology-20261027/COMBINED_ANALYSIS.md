# Combining Mystic Rebels and LOOKS-LIKE-COSTAR
## Source-grounded findings and a natal-first integration proposal

Reviewed 27 October 2026. This report answers the user's request for additional similarities and useful ways to combine the two systems. It is analysis, not an implementation or an empirical validation of astrology or numerology.

**There is enough shared structure and complementary information to design a substantially richer combined view. Daily numerology is optional. The strongest approach is to compare a number's specific role and meaning with a fully contextualized natal factor—not to assign one planet to each digit.**

The most valuable discoveries are: distinct kinds of structure in 4 and 8; exploration/wisdom in 5; precision and fairness in 2; management and care in 6; analysis and intuition in 7; retained letter identity below the root number; and directional explanations already present in both repositories.

## 1. What was actually reviewed

| Repository | Inspected version | Scope |
|---|---|---|
| [LOOKS-LIKE-COSTAR](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/tree/023140de4ac9ebad8a804b4c984337135e77b19a) | main, 023140de4ac9ebad8a804b4c984337135e77b19a | Complete recursive tree: 102 files, all downloaded as a source-text snapshot. Deep review of the natal calculators, PMEI, name/letter engine, all 15 astrology knowledge-base files, four astrology-data modules, relationship structures, app routing, and relevant interpretation/rectification code. Large repetitive numerology banks were selectively read; UI files outside relevant flows were inventoried/searched rather than all read in full. |
| [Mystic Rebels](https://github.com/olsonan26/mystic-rebels-chart-generator/tree/3d83db75c30b26d9b068576d84ec49554822fd8c) | codex/methodology-verification-20261024, 3d83db75c30b26d9b068576d84ec49554822fd8c | Calculation and placement logic, source-authority guides, interpretation inventory, source-reviewed sign/Chiron/Eunomia profiles, selected original assertions and retained source passages. This did not repeat the entire original-image audit. |

GitHub branch identities were checked directly. Mystic's default main is the older e250662 snapshot; its README directs interpretation work to the audited branch. Existing local location/API edits were preserved. Neither repository was modified or deployed.

Detailed coverage and source links appear in [numerology findings](numerology-findings.md), [Costar astrology findings](costar-astrology-findings.md), [Mystic findings](mystic-rebels-findings.md), and the [snapshot manifest](source-snapshot.json).

## 2. The strongest number-to-theme connections

**Every link in the following table is a proposed thematic correspondence.** The source meanings on each side are present in the repositories; the bridge between them is our analytical proposal. These are not discovered statistical correlations or established rules saying a number equals a planet/sign/house.

| Number | Specific meaning in LOOKS-LIKE-COSTAR | Mystic components worth comparing | Detail the combined view could add |
|---|---|---|---|
| **1** | Initiation, independent direction, will, leadership and strategy | Mars: action/initiative; Sun: purpose/expression; H1: autonomy | Distinguish starting, taking action and being visible. These are related functions, not interchangeable traits. |
| **2** | Cooperation and sensitivity, but also precision, quality, fairness and justice | Venus/Libra: exchange and weighing perspectives; Mercury/Virgo: discernment/refinement; Moon where emotional safety is the actual theme | A justice-oriented 2 and a sensitive 2 need different comparisons. Its career bank includes quality assurance and technical precision, so reducing it to emotionality loses information. |
| **3** | Creative expression, performance, voice, play and sensitivity to response | Sun/Leo/H5: creative vitality and expression; Mercury/Gemini/H3: communicating information | Separate creativity from communication. Performance, teaching and explaining need not have the same chart context. |
| **4** | Craft, reliable methods, exactness, durable construction and loyalty | Saturn: discipline and sustained work; Taurus: tangible grounding; Virgo/H6: refinement and practical method | The central question is how something is built and maintained. It is not automatically a fourth-house/home signature. |
| **5** | Freedom, variety, persuasion, exploration, learning through experience | Jupiter/Sagittarius/H9: experience, exploration and wisdom; Mercury/Gemini/H3: options and exchange; Uranus only for reworking systems | A particularly useful non-obvious match: the number bank explicitly says experience becomes wisdom. That makes Jupiter/Sagittarius a serious candidate, alongside Mercury; 5 should not be reduced to Uranus. |
| **6** | Care, stewardship, responsibility, harmony, home, beauty and management | Moon/Cancer/H4: nurture/safety; Venus: connection/design; Saturn: duty/management | Distinguish caring for someone, organizing support, creating beauty and assuming responsibility. The same apparent “care” can have different functions. |
| **7** | Research, truth-seeking, refined standards, privacy, depth and intuition | Mercury/Virgo for analysis; Pluto/Scorpio for hidden depth; Neptune/Pisces for unknown/spiritual themes | Choose the subtheme first. Analytical inquiry is different from spiritual receptivity. “7 = Neptune” would erase that distinction. |
| **8** | Executive strategy, authority, governance, resources, ethical responsibility and outcomes | Saturn/H10: authority/accomplishment; Venus/H2 for resources/value; Pluto where power is specifically involved | Distinguish executive authority from money and from control. An 8 is not automatically eighth-house/Scorpio; public accomplishment often points to a different field. |
| **9** | Humane service, broad synthesis, compassion, boundaries, completion and release | H6 for practical service; H11 for collective contribution; H12/Pisces for release; broader philosophical context only when present | Service, public contribution and letting go are different expressions. The shared digit does not establish a ninth-house correspondence. |

Number sources: [compact number meanings](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L51-L61), [natal role-specific banks](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/data.ts#L1301-L1360), [name-number narratives](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/nameNumberDescriptions.ts), [first/called/full-name roles](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/numbers.ts).

Mystic sources: [planet and house vocabularies](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/docs/PROFILE_REPORT_KNOWLEDGE_PATH.md#L249-L273), [reviewed sign profiles](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/data/knowledge/source_meaning_profiles.json). Signs here supply contextual expression styles; they are not complete personality descriptions.

### Why the 4-versus-8 finding matters

Both share Saturn-like responsibility and structure. However, 4 emphasizes craft, exactness and dependable process; 8 emphasizes strategic direction, authority and consequential outcomes. PMEI itself places letter-value 4 in Physical and 8 in Mental.

A useful combined comparison could therefore distinguish hands-on building from directing a system, even when both refer to similar Saturn themes. That is more informative than treating every structural number as the same archetype.

The 6-versus-9 distinction is similarly useful: 6 emphasizes sustained care and stewardship; 9 adds broader service, completion and release. Both can concern helping people, but their proposed functions differ.

## 3. Additional similarities and opportunities beyond a digit table

### A. The same number can occupy different psychological roles

The calculator distinguishes Expression, Soul Urge, Birth Force, Ultimate Goal, Balance and Called Name; PMEI is a separate count-based system. An 8 Soul Urge, an 8 Expression, an 8 Called Name and a Mental count of 8 are different features.

A combined system can compare:
- **Inner motive:** what the numerology prose describes as wanted or valued.
- **Expression/capability:** how a theme is represented as being expressed.
- **Social presentation:** how the called-name text describes reception by others.
- **Life context:** where the natal field locates the relevant theme.
- **Operating channel:** what PMEI's literal counts and rules describe.

Do not declare Soul Urge equal to Moon, Expression equal to Sun, or Called Name equal to Ascendant. Those are possible role comparisons, not equivalent calculations. [Core feature definitions](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L254-L332).

### B. PMEI and astrology can be complementary maps

PMEI bins are Physical={4,5}, Mental={1,8}, Emotional={2,3,6}, Intuitive={7,9}. Each eligible letter adds one count; the counts are not weighted sums or digit-reduced totals.

This creates useful distinctions:
- 4 and 8 share structural meanings but sit in different channels.
- 5 is Physical although its text includes communication and adaptation.
- 7 is Intuitive although much of its text concerns research and analysis.
- 3 is Emotional although its expression can involve language and performance.

Consequently, **Physical=Earth, Mental=Air, Emotional=Water, Intuitive=Fire is unsupported**. A better comparison keeps both maps separate and asks how a channel theme relates to specific planetary functions and their chart context. [PMEI definitions](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L5-L61).

### C. Letter identity preserves detail that root numbers erase

B, K and T all have value 2, but the name library gives them different meanings: gentle mediation, creative/intuitive strategy, and fairness/listening respectively. It also records first/middle/last roles, strengths, difficult expressions and action verbs.

This could allow much finer comparison: a particular letter's inventive quality might overlap with innovation, while another letter of the same number overlaps with negotiation. The shared root does not require the same planetary association.

Some of that rich data is not currently used: the engine consumes only the first matching adjacent pair, ignores its three declared trio rules, and often uses generic micro-text instead of the dedicated positional prose. This is an opportunity in the saved material, not a completed feature. [Letter library](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/letters.ts), [active cue engine](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L81-L104).

### D. Both systems already contain perspective-aware relationships

The numerology love bank has **81 ordered 1–9 pair entries**. Its 4→5 and 5→4 narratives differ. The astrology FREE matrix has **132 directed sign relationships**, excluding same-sign entries; Aries→Gemini differs from Gemini→Aries.

This is a concrete shared design: explain what each side contributes, receives or needs separately. It can support relationship comparisons without a single compatibility percentage. A number pair is still not a calculated angular aspect. [Number relationships](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/loveDescriptions.ts), [directional FREE matrix](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/alchemistic_astrology_knowledge_base/core_frameworks/free_theory_matrix.ts).

### E. Career and relationships can be compared in separate contexts

The older astrology material separates ambition/public position, H10 structure, H6 work routines and H2 resources. Its relationship framework separates H2 value, H5 joy, H7 exchange and H8 intimacy.

These distinctions make a useful combined view possible:
- What kind of task or expression does the numerology text emphasize?
- Where does the natal chart place the relevant function?
- Does the overlap concern work method, public responsibility, resources, care, enjoyment or intimacy?

Exact meanings and any composite interpretation still need the audited Mystic source. Do not treat legacy lists of “healthy” or “adverse” placements as validated relationship outcomes. [Vocational framework](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/alchemistic_astrology_knowledge_base/core_frameworks/vocational_synthesis.ts), [relationship framework](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/alchemistic_astrology_knowledge_base/core_frameworks/synastry.ts).

### F. Empty diagrams do not necessarily describe absent capacity

The PMEI material describes zero planes as an all-or-nothing switch, not a missing human capacity. Mystic says an empty house retains its field, sign and ruler context.

That is a meaningful shared interpretive caution. It does not establish a correlation between zero planes and empty houses, or give them identical meanings. [PMEI source](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L5-L13), [empty-house concept](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/docs/PROFILE_REPORT_KNOWLEDGE_PATH.md#L276).

### G. Contrasts may add more detail than agreement

A Soul Urge theme of connection alongside Expression themes of authority may be more informative than two descriptions both saying “responsible.” The natal view could distinguish value exchange from public duty instead of smoothing them into one trait.

Likewise, a structural 4 theme alongside exploration themes does not invalidate either system. It creates a specific question about security, method, freedom and context. A combined view should allow reinforcement, complementarity, tension and **no supported relationship**.

Mystic's WITH/WHILE distinction is useful here: thematic overlap across systems is a proposed semantic connection, not a physical contact or proof of causation. Extending this distinction across numerology is our design proposal. [Source composition boundaries](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/docs/METHODOLOGY_SOURCE_REVIEW.md#L112).

### H. There are additional philosophy-level research leads

Mystic's Self12/1/2, Personal3/4/5, Others6/7/8 and World9/10/11 house groupings could contextualize inward, close-personal, relational and collective expressions. This is more nuanced than identifying numerological9 with H9.

Its Mutable→Cardinal→Fixed teaching sequence also suggests a candidate process comparison with adaptation, initiation and sustained building. The familiar 5/1/4 themes could be investigated against those functions; this is not a source rule equating the numbers with modes.

Node integration offers another dialogue about using both sides of a polarity, rather than abandoning one side. It does not make Ultimate Goal a North Node or prove past-life biography. [Mystic original assertions](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/data/knowledge/original_assertions.json#L3561-L3680), [node framework](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/alchemistic_astrology_knowledge_base/core_frameworks/nodes_integration.ts).

## 4. What a richer comparison would look like

These are hypothetical design examples, not readings of actual people or approved source-combination rules.

**Same 5, different expression:** one comparison might find an exploration/experience theme alongside Jupiter in an H9 context. Another might find variety/persuasion alongside Mercury in H3. Both overlap with portions of the number5 text, but they suggest different inquiry: wider experience versus immediate information exchange.

**Inner cooperation, outward executive direction:** Soul Urge2 and Expression8 could frame a question about valuing partnership while organizing outcomes. Relevant Venus and Saturn contexts would refine that question. The system should not invent a history of conflict or assume that the tension exists in the person's life.

**Same root2, different letters:** a root2 built from B, K or T does not erase their different authored letter meanings. A future comparison could preserve that detail, the letter's position and the number's role before examining refinement, fairness or innovation in the chart.

The practical gain is specificity: “what theme, in which role, through which function, in which life area, expressed how?” The output should show the ingredients and leave room for the person's actual experience.

## 5. Corrections and cautions from the uploaded answer

1. **LOOKS-LIKE-COSTAR already contains explicitly Alchemistic material.** PHSR, Whole Signs, modern rulers, FREE directionality and delegate concepts are genuine shared architecture. Calling its entire astrology knowledge base conventional understates that overlap.
2. **The supplied hierarchy is incomplete shorthand.** Mystic's reviewed advanced order is Planet→House→Degree→Decan→Aspects→Sign→Ruler, with sign technically assessed earlier for intermediate layers. Its complete contextual interpretation assembler is not implemented. [Source review](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/docs/METHODOLOGY_SOURCE_REVIEW.md#L112).
3. **Daily timing is not a prerequisite.** A natal/name comparison can precede transits, progressions, Spark and the full advanced aspect network.
4. **The older astrology screen is source material, not a verified running integration.** In this snapshot App.tsx does not import/render AstrologyScreen. That screen itself sends chart images and serialized knowledge to Gemini. No hosted version was tested. [Entrypoint](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/App.tsx), [screen knowledge assembly](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/AstrologyScreen.tsx#L290-L387).
5. **Existing source conflicts require explicit choices.** Older Chiron interpretations must give way to reviewed Mystic “Fractured Structures” vocabulary. Solar Arc rectification advice conflicts with the source exclusion. Symmetric orb checks are not the directional PURE procedure. Eunomia alternatives remain separate. See the detailed astrology conflict table.
6. **Numerology has internal method differences.** Ultimate Goal combines a birthday component with full-name Expression even though some internal fields call it Life Path. Vowel handling, master-number preservation and middle-name inclusion differ across modules. Do not silently normalize them. [Core formulas](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L254-L391).

## 6. Recommended first combination

Build a natal/name comparison layer around the existing systems:

1. **Keep their calculations separate.** Mystic supplies astronomical positions, fields/True Placement, Tone, Pulse and uncertainty. Numerology supplies role-specific values, reduction chains, literal letters/name basis and PMEI counts.
2. **Use a small, versioned correspondence library.** Begin with narrow themes such as precision, exploration, care, authority, expression and humane closure. Each record carries its two source meanings, required context, why the bridge was proposed and its hypothesis status.
3. **Compare within a chosen life domain.** Communication, creative process, work organization and inner-versus-public expression are suitable starting areas. Preserve sources and disagreements; do not use a loose keyword overlap as a finished interpretation.
4. **Show missing context honestly.** Unknown birth time cannot support invented houses/angles. Unresolved Spark, aspects and progressions remain absent. Mystic currently reports zero ready personal-report sections out of18; a research comparison is not permission to bypass those report gates.
5. **Study actual associations separately.** Freeze proposed mappings before testing, compare independently calculated cases, keep a holdout set, use suitable shuffled/matched baselines and account for many comparisons.

Multiple name-derived numbers are related transformations of the same letters. Several birthday features share birth-date information with astrology. H6 and its True Placement label are not independent observations. Repeated words and arithmetic relatives must not be advertised as multiple confirmations.

**Feasibility conclusion:** the repositories support a substantive natal-first comparison with much more nuance than a fixed correspondence chart. They do not yet establish that a particular number occurs unusually often with a particular placement, or that merging their meanings improves predictive accuracy. The concrete next step is a carefully sourced comparison library and a reviewable natal example, with daily calculations left optional.

