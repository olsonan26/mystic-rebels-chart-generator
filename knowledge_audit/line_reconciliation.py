"""Locate each OCR line against the immutable PDF; never approve its transcription.

Matching is lexical only. Glyphs, numbers, diagrams, negation and source authority
still require image review. Raw source text stays in ignored reference/ files.
"""
import hashlib
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher


def text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def tokens(text):
    # Preserve numeric tokens and degree/prime glyphs, including OCR mistakes.
    return [(m.group().casefold(),m.start(),m.end()) for m in
            re.finditer(r"\d+|[^\W\d_]+|[°′'″:]",text,re.UNICODE)]


def grams(words):
    return set(zip(words,words[1:],words[2:]))


def page_index(pages):
    index=defaultdict(set)
    for page,text in pages.items():
        for gram in grams([v for v,s,e in tokens(text)]):
            index[gram].add(page)
    return index


def rank_pages(words,index,limit=3):
    hits=Counter()
    for gram in grams(words):
        for page in index.get(gram,[]): hits[page]+=1
    return sorted(hits.items(),key=lambda x:(-x[1],x[0]))[:limit]


def line_box(line):
    words=line.get('words',[])
    if not words: return None
    x=min(w['x'] for w in words); y=min(w['y'] for w in words)
    return [x,y,max(w['x']+w['width'] for w in words)-x,
            max(w['y']+w['height'] for w in words)-y]


def reconcile(ocr,pages,index,page_hashes):
    raw_lines=ocr['lines']; source=[]; ranges=[]
    for line in raw_lines:
        start=len(source); source.extend(v for v,s,e in tokens(line['text']))
        ranges.append((start,len(source)))
    ranked=rank_pages(source,index)
    # A photographed page may straddle reflowed PDF pages. Candidate anchors
    # farther away remain separate leads, not part of a fabricated continuous span.
    selected=sorted({p for anchor,score in ranked[:1] for p in range(anchor-1,anchor+2) if p in pages})
    target=[]; locations=[]
    for page in selected:
        for value,start,end in tokens(pages[page]):
            target.append(value); locations.append((page,start,end))
    mapped={}
    for block in SequenceMatcher(None,source,target,autojunk=False).get_matching_blocks():
        if block.size>=3:
            for offset in range(block.size): mapped[block.a+offset]=block.b+offset
    public=[]; private=[]
    for ordinal,(line,(start,end)) in enumerate(zip(raw_lines,ranges),1):
        mapped_tokens=[mapped[i] for i in range(start,end) if i in mapped]
        count=end-start
        fraction=len(mapped_tokens)/max(1,count)
        status='AUTO_MATCH_CANDIDATE' if count and fraction==1 else 'AUTO_PARTIAL_CANDIDATE' if mapped_tokens else 'NO_MATCH_CANDIDATE'
        spans=[]
        for page in sorted({locations[i][0] for i in mapped_tokens}):
            positions=[locations[i] for i in mapped_tokens if locations[i][0]==page]
            spans.append(dict(pdf_page=page,char_start=min(p[1] for p in positions),
                char_end=max(p[2] for p in positions),page_text_sha256=page_hashes[page]))
        item=dict(line_number=ordinal,line_sha256=text_hash(line['text']),bbox=line_box(line),
            tokens=count,matched_tokens=len(mapped_tokens),pdf_spans=spans,
            comparison_status=status,visual_transcription_status='PENDING',
            review_flags=(['NUMERIC_OR_GLYPH_PRESENT'] if any(c.isdigit() for c in line['text']) else [])+
                (['SHORT_OR_FIGURE_LINE'] if count<4 else [])+
                (['UNMATCHED_TEXT_NOT_PROVEN_OMISSION'] if fraction<1 else []))
        public.append(item)
        private.append(dict(**item,source_text=line['text'],candidate_pdf_text=[
            dict(pdf_page=s['pdf_page'],text=pages[s['pdf_page']][s['char_start']:s['char_end']]) for s in spans]))
    return public,private,ranked


def header_candidates(ocr):
    candidates=[]
    for n,line in enumerate(ocr['lines'],1):
        box=line_box(line)
        if box and box[1] < ocr['height']*.16:
            text=line['text'].strip()
            for number in re.findall(r'(?<!\d)\d{1,4}(?!\d)',text):
                candidates.append(dict(value=number,line_number=n,bbox=box,
                    status='OCR_HEADER_CANDIDATE_NOT_VISUALLY_VERIFIED'))
    return candidates


def validate_annotation(note,row,ocr):
    if note['image_sha256']!=row['content_sha256'] or note['ocr_output_sha256']!=row['ocr_output_sha256']:
        raise ValueError('Visual line annotation provenance drift')
    for start,end in note['line_ranges']:
        if start<1 or end<start or end>len(ocr['lines']):
            raise ValueError('Visual annotation outside OCR line range')
    if not note.get('finding') or not note.get('printed_header'):
        raise ValueError('Visual annotation requires an inspected header and finding')
