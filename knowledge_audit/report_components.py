"""Cited chart annotations, separated from unvalidated personal interpretations.

No astronomical calculation, trait inference, prediction or conflict selection.
Inputs are caller-supplied chart facts; output attaches source vocabulary only.
"""
from collections import Counter

SIGNS=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')


def usage_catalog(inventory, assertions, findings, meaning_profiles=None):
    rows=[]
    for record in inventory['records']:
        identity=record['id']
        claims=[a for a in assertions['assertions'] if a['concept_id']==identity]
        issues=[f for f in findings['findings'] if identity in f['concept_ids']]
        compiled=[dict(kind='COMPILED_PDF',**w) for w in record.get('witnesses',[])]
        originals=[dict(kind='ORIGINAL_ASSERTION_WITNESS',assertion_id=a['id'],
            proposition=a['proposition'],**w) for a in claims for w in a['witnesses']]
        citations=compiled+originals
        vocabulary=(identity.startswith(('meaning-','field-','asteroid-')) or identity=='chiron') and record['kind']=='meaning'
        allowed=vocabulary and record['source_status']=='PASSAGE_REVIEWED' and bool(citations)
        status=('CITED_VOCABULARY_ANNOTATION_AVAILABLE' if allowed else
            'CONFLICT_REFERENCE_ONLY' if record['source_status'] in ('CONFLICT','SEMANTIC_TENSION') else
            'INCOMPLETE_REFERENCE_ONLY' if vocabulary else 'CONTEXT_OR_TECHNIQUE_REFERENCE_ONLY')
        rows.append(dict(concept_id=identity,title=record['title'],source_status=record['source_status'],
            source_excerpt_allowed=bool(citations),chart_vocabulary_annotation_allowed=allowed,
            personal_trait_claim_allowed=False,completed_personal_report_approved=False,
            use_status=status,source_meaning=record['meaning_summary'],
            exceptions=record.get('exceptions',[]),dependencies=record.get('requires_concepts',[]),
            report_gap=record.get('report_gap',''),citations=citations,findings=issues,
            source_assertion_ids=[a['id'] for a in claims]))
    if meaning_profiles is not None:
        if meaning_profiles.get('generic_library_fallback_allowed') is not False:
            raise ValueError('Source profiles must prohibit unaudited library fallback.')
        lookup={r['concept_id']:r for r in rows}
        seen_profiles=set()
        for profile in meaning_profiles['profiles']:
            identity=profile['concept_id']
            if identity in seen_profiles:raise ValueError('Duplicate source meaning profile: '+identity)
            seen_profiles.add(identity)
            if profile.get('personal_answer_approved') is not False or not profile.get('citations'):
                raise ValueError('A source profile needs citations and cannot approve personal answers.')
            base=lookup.get(identity,{})
            entry=dict(base)
            entry.update(concept_id=identity,title=profile['title'],source_profile_id=profile['id'],
                source_status=base.get('source_status','ORIGINAL_PASSAGE_REVIEWED'),
                source_concept_id=profile['source_concept_id'],source_meaning=profile['source_meaning'],
                source_excerpt_allowed=True,citations=profile['citations']+profile.get('context_citations',[]),
                retained_other_citations=base.get('citations',[]),dependencies=profile['dependencies'],
                exceptions=list(dict.fromkeys(base.get('exceptions',[])+profile['exceptions'])),
                findings=base.get('findings',[]),personal_trait_claim_allowed=False,
                completed_personal_report_approved=False,external_library_fallback_allowed=False,
                report_gap='Full contextual personal synthesis remains unapproved; this scoped source vocabulary is available.',
                source_assertion_ids=base.get('source_assertion_ids',[]))
            if profile['vocabulary_status']=='CONFLICTING_ORIGINAL_MEANINGS_BOTH_RETAINED':
                alternatives=profile.get('alternatives',[])
                if len(alternatives)<2 or profile.get('selected_alternative_id') is not None or not all(a.get('citations') for a in alternatives):
                    raise ValueError('Conflicting meanings must retain cited alternatives without selecting one.')
                entry.update(chart_vocabulary_annotation_allowed=False,chart_alternatives_annotation_allowed=True,
                    use_status='CONFLICT_ALTERNATIVES_AVAILABLE',alternatives=alternatives,selected_alternative_id=None)
            elif profile['vocabulary_status']=='ORIGINAL_PASSAGE_REVIEWED':
                entry.update(chart_vocabulary_annotation_allowed=True,chart_alternatives_annotation_allowed=False,
                    use_status='CITED_VOCABULARY_ANNOTATION_AVAILABLE_WITH_SCOPED_LIMITS' if identity=='chiron' else 'CITED_VOCABULARY_ANNOTATION_AVAILABLE',
                    held_out_finding_ids=profile.get('held_out_finding_ids',[]),
                    rejected_fallback_meanings=profile.get('rejected_fallback_meanings',[]))
            else:raise ValueError('Unrecognized vocabulary profile status.')
            if identity in lookup:rows[rows.index(base)]=entry
            else:rows.append(entry)
            lookup[identity]=entry
    for row in rows:row['external_library_fallback_allowed']=False
    missing=[s for s in SIGNS if not any(r['concept_id']=='sign-'+s.lower() and r['chart_vocabulary_annotation_allowed'] for r in rows)]
    return dict(schema_version='1.1',scope='PER_COMPONENT_SOURCE_USE_NOT_PERSONAL_REPORT_APPROVAL',
        allowed_operations=['Read and cite source vocabulary, including qualified discussion of conflicting sources.',
            'Attach eligible vocabulary to caller-supplied natal chart facts without claiming it describes the person.'],
        prohibited_operations=['Promote annotations to established personal traits or a validated full report.',
            'Choose a conflicting definition, invent missing sign meanings, or execute unresolved formulas.'],
        canonical_NOT_APPROVED_means='Not approved for personal interpretation; it does not forbid reading/citing the source as source material.',
        source_text_kind='REVIEWED_AUDIT_SUMMARIES_NOT_VERBATIM_BOOK_QUOTES',
        counts=dict(total_components=len(rows),annotation_available=sum(r['chart_vocabulary_annotation_allowed'] for r in rows),
            conflict_alternatives_available=sum(r.get('chart_alternatives_annotation_allowed',False) for r in rows),
            statuses=dict(Counter(r['use_status'] for r in rows))),components=rows,
        missing_sign_dictionary=missing,core_sign_entries_present=12-len(missing),exhaustive_all_sign_rules_complete=False,
        external_library_fallback_allowed=False,
        consumer_requirements={'replace_existing_source_meanings_for':['all twelve sign core entries','Chiron','Eunomia alternatives'],
            'on_missing_or_conflicting_source':'Display source evidence and limitations; never silently use an existing/generic library.'},
        complete_personal_report_approved=False)


def body_concept(body, by_id):
    candidates=('meaning-'+body.lower(),'asteroid-'+body.lower(),body.lower())
    return next((identity for identity in candidates if identity in by_id),None)


def annotate_chart(request, catalog):
    if not isinstance(request,dict) or set(request)-{'chart_context','placements'}:
        raise ValueError('Provide only chart_context and placements; do not supply interpretation instructions.')
    if request.get('chart_context')!='natal':
        raise ValueError('This annotation mode supports natal chart facts only; other contexts need separate rules.')
    placements=request.get('placements')
    if not isinstance(placements,list) or not 1<=len(placements)<=100:
        raise ValueError('Provide 1-100 chart placements.')
    by_id={r['concept_id']:r for r in catalog['components']}
    annotations=[];gaps=[];seen=set()
    for fact in placements:
        if not isinstance(fact,dict) or set(fact)-{'body','sign','house'}:
            raise ValueError('Each placement accepts body, sign and house only.')
        body=fact.get('body')
        if not isinstance(body,str) or not body.isalpha() or len(body)>40:
            raise ValueError('Body must be a simple named chart object.')
        if body.casefold() in seen:raise ValueError('Duplicate body: '+body)
        seen.add(body.casefold())
        house=fact.get('house');sign=fact.get('sign')
        if house is not None and (type(house) is not int or not 1<=house<=12):
            raise ValueError('House must be an integer1-12 or null; never invent an unknown house.')
        if sign is not None and sign not in SIGNS:raise ValueError('Unknown sign name.')
        identity=body_concept(body,by_id)
        sign_id='sign-'+sign.lower() if sign is not None else None
        ids=([identity] if identity else [])+([f'field-{house:02d}'] if house is not None else [])+([sign_id] if sign_id in by_id else [])
        components=[];alternatives=[];references=[]
        if not identity:gaps.append(dict(body=body,kind='UNKNOWN_BODY',detail='No source vocabulary record; no fallback invented.'))
        for concept in ids:
            item=by_id[concept]
            if item['chart_vocabulary_annotation_allowed']:
                components.append(dict(concept_id=concept,source_text=item['source_meaning'],
                    wording='In this source: '+item['source_meaning'],citations=item['citations'],
                    exceptions=item['exceptions'],dependencies=item['dependencies'],
                    findings=item['findings'],report_gap=item['report_gap']))
            elif item.get('chart_alternatives_annotation_allowed'):
                alternatives.append(dict(concept_id=concept,alternatives=item['alternatives'],selected_alternative_id=None,
                    findings=item['findings'],exceptions=item['exceptions'],external_library_fallback_allowed=False))
                gaps.append(dict(body=body,concept_id=concept,kind='UNRESOLVED_SOURCE_ALTERNATIVES',
                    detail='Both source meanings are included; no precedence or generic substitute is selected.'))
            else:
                if item['source_excerpt_allowed']:
                    references.append(dict(concept_id=concept,source_text=item['source_meaning'],citations=item['citations'],
                        exceptions=item['exceptions'],findings=item['findings'],use_status=item['use_status']))
                gaps.append(dict(body=body,concept_id=concept,kind=item['use_status'],
                    detail=item['report_gap'],findings=item['findings'],reference_meaning=item['source_meaning'],
                    reference_citations=item['citations'],reference_exceptions=item['exceptions'],
                    note='Reference only; no single resolved chart interpretation has been selected.'))
        if sign is not None and sign_id not in by_id:gaps.append(dict(body=body,kind='SIGN_VOCABULARY_NOT_COMPLETE',sign=sign,
            detail='Sign preserved as a chart fact; no sign interpretation or sign/body synthesis generated.'))
        annotations.append(dict(chart_fact=dict(fact),fact_provenance='CALLER_SUPPLIED_NOT_RECALCULATED_OR_INDEPENDENTLY_VERIFIED',
            source_vocabulary=components,source_alternatives=alternatives,source_references=references,
            external_library_fallback_allowed=False,combined_personal_interpretation=None))
    return dict(scope='CITED_NATAL_CHART_VOCABULARY_ANNOTATIONS',status='ANNOTATIONS_WITH_EXPLICIT_GAPS' if gaps else 'ANNOTATIONS_ONLY',
        annotations=annotations,gaps=gaps,personal_report_generated=False,personal_traits_inferred=False,
        astronomical_input_verified=False,empirical_accuracy_validated=False,
        external_library_fallback_allowed=False,
        synthesis_limit='These are separate source meanings attached to supplied placements, not a combined interpretation of a person.')


def render_markdown(packet):
    lines=['# Cited chart vocabulary annotations','',packet['synthesis_limit'],'',
        'Vocabulary below is reviewed audit summary text, not verbatim quotation from the book.','',
        'Chart facts were supplied by the caller and were not recalculated or independently verified.','']
    for row in packet['annotations']:
        fact=row['chart_fact'];parts=[fact['body']]
        if fact.get('sign') is not None:parts.append(fact['sign'])
        if fact.get('house') is not None:parts.append('house '+str(fact['house']))
        lines+=['## '+', '.join(parts),'']
        for component in row['source_vocabulary']:
            refs=[]
            for citation in component['citations']:
                if citation['kind']=='COMPILED_PDF':
                    refs.append(citation['source_id']+', PDF page '+str(citation['pdf_page']))
                else:refs.append(citation.get('assertion_id',citation.get('name','Original'))+', original file '+citation['file_id']+
                    (', printed '+','.join(citation['original_printed_pages']) if citation.get('original_printed_pages') else ''))
            lines += [component['wording'],'','Sources: '+'; '.join(dict.fromkeys(refs))+'.','']
            if component['exceptions']:lines+=['Source limits: '+'; '.join(component['exceptions']),'']
            lines+=['Required context: '+', '.join(component['dependencies'])+'.',
                'Unfinished synthesis: '+component['report_gap'],'']
            if component['findings']:lines+=['Linked findings: '+', '.join(f['id'] for f in component['findings'])+'.','']
        for conflict in row['source_alternatives']:
            lines+=['Unresolved source alternatives; neither definition has been selected.','']
            for alternative in conflict['alternatives']:
                lines += [alternative['label']+': '+alternative['source_meaning'],'',
                    'Sources: '+'; '.join(c.get('name',c['file_id'])+', printed '+','.join(c.get('original_printed_pages',[])) for c in alternative['citations'])+'.','']
        for reference in row['source_references']:
            lines+=['Source reference with unresolved coverage: '+reference['source_text'],'',
                'Source IDs: '+'; '.join(c.get('file_id',c.get('source_id','')) for c in reference['citations'])+'.','']
    if packet['gaps']:
        lines+=['## Unresolved components','']
        lines+=['- '+g['body']+': '+g['kind']+'. '+g.get('detail','') for g in packet['gaps']]
    lines+=['','Consumer rule: do not replace these source meanings or their gaps with an existing or generic astrology library.']
    return '\n'.join(lines).rstrip()+'\n'
