"""Cited chart annotations, separated from unvalidated personal interpretations.

No astronomical calculation, trait inference, prediction or conflict selection.
Inputs are caller-supplied chart facts; output attaches source vocabulary only.
"""
from collections import Counter

SIGNS=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')


def usage_catalog(inventory, assertions, findings):
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
    return dict(schema_version='1.0',scope='PER_COMPONENT_SOURCE_USE_NOT_PERSONAL_REPORT_APPROVAL',
        allowed_operations=['Read and cite source vocabulary, including qualified discussion of conflicting sources.',
            'Attach eligible vocabulary to caller-supplied natal chart facts without claiming it describes the person.'],
        prohibited_operations=['Promote annotations to established personal traits or a validated full report.',
            'Choose a conflicting definition, invent missing sign meanings, or execute unresolved formulas.'],
        canonical_NOT_APPROVED_means='Not approved for personal interpretation; it does not forbid reading/citing the source as source material.',
        source_text_kind='REVIEWED_AUDIT_SUMMARIES_NOT_VERBATIM_BOOK_QUOTES',
        counts=dict(total_components=len(rows),annotation_available=sum(r['chart_vocabulary_annotation_allowed'] for r in rows),
            statuses=dict(Counter(r['use_status'] for r in rows))),components=rows,
        missing_sign_dictionary=list(SIGNS),complete_personal_report_approved=False)


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
        ids=([identity] if identity else [])+([f'field-{house:02d}'] if house is not None else [])
        components=[]
        if not identity:gaps.append(dict(body=body,kind='UNKNOWN_BODY',detail='No source vocabulary record; no fallback invented.'))
        for concept in ids:
            item=by_id[concept]
            if item['chart_vocabulary_annotation_allowed']:
                components.append(dict(concept_id=concept,source_text=item['source_meaning'],
                    wording='In this source: '+item['source_meaning'],citations=item['citations'],
                    exceptions=item['exceptions'],dependencies=item['dependencies'],
                    findings=item['findings'],report_gap=item['report_gap']))
            else:
                gaps.append(dict(body=body,concept_id=concept,kind=item['use_status'],
                    detail=item['report_gap'],findings=item['findings'],reference_meaning=item['source_meaning'],
                    reference_citations=item['citations'],reference_exceptions=item['exceptions'],
                    note='Reference only; no single resolved chart interpretation has been selected.'))
        if sign is not None:gaps.append(dict(body=body,kind='SIGN_VOCABULARY_NOT_COMPLETE',sign=sign,
            detail='Sign preserved as a chart fact; no sign interpretation or sign/body synthesis generated.'))
        annotations.append(dict(chart_fact=dict(fact),fact_provenance='CALLER_SUPPLIED_NOT_RECALCULATED_OR_INDEPENDENTLY_VERIFIED',
            source_vocabulary=components,combined_personal_interpretation=None))
    return dict(scope='CITED_NATAL_CHART_VOCABULARY_ANNOTATIONS',status='ANNOTATIONS_WITH_EXPLICIT_GAPS' if gaps else 'ANNOTATIONS_ONLY',
        annotations=annotations,gaps=gaps,personal_report_generated=False,personal_traits_inferred=False,
        astronomical_input_verified=False,empirical_accuracy_validated=False,
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
                else:refs.append(citation['assertion_id']+', original file '+citation['file_id'])
            lines += [component['wording'],'','Sources: '+'; '.join(dict.fromkeys(refs))+'.','']
            if component['exceptions']:lines+=['Source limits: '+'; '.join(component['exceptions']),'']
            lines+=['Required context: '+', '.join(component['dependencies'])+'.',
                'Unfinished synthesis: '+component['report_gap'],'']
            if component['findings']:lines+=['Linked findings: '+', '.join(f['id'] for f in component['findings'])+'.','']
    if packet['gaps']:
        lines+=['## Unresolved components','']
        lines+=['- '+g['body']+': '+g['kind']+'. '+g.get('detail','') for g in packet['gaps']]
    return '\n'.join(lines).rstrip()+'\n'
