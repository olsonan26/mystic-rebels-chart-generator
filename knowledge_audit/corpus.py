"""Local, page-preserving research retrieval with explicit extraction provenance.

Stored text is source data, never executable instructions or approved rules.
An extracted/searchable page is not a semantically reviewed or implemented page.
"""
import hashlib
import re
import sqlite3
from pathlib import Path

def index_pdf(pdf_path, database_path, source_id):
    from pypdf import PdfReader
    pdf_path, database_path = Path(pdf_path), Path(database_path)
    sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    reader = PdfReader(pdf_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY, sha256 TEXT NOT NULL, pages INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS pages(source_id TEXT, pdf_page INTEGER, text TEXT NOT NULL, text_sha256 TEXT NOT NULL, review_status TEXT NOT NULL, PRIMARY KEY(source_id,pdf_page));
        CREATE VIRTUAL TABLE IF NOT EXISTS passages USING fts5(source_id UNINDEXED,pdf_page UNINDEXED,text,tokenize='unicode61');
        ''')
        old = db.execute('SELECT sha256 FROM sources WHERE id=?',(source_id,)).fetchone()
        if old and old[0] != sha:
            raise ValueError('Source changed: assign a new version ID; do not overwrite provenance')
        if old:
            indexed = db.execute('SELECT pdf_page,text,text_sha256 FROM pages WHERE source_id=? ORDER BY pdf_page', (source_id,)).fetchall()
            if len(indexed) != len(reader.pages):
                raise ValueError('Existing source page accounting is corrupt; preserve it for inspection')
            for (number, text, text_hash), page in zip(indexed, reader.pages):
                expected = re.sub(r'\s+', ' ', page.extract_text() or '').strip()
                if (number < 1 or number > len(reader.pages) or text != expected
                        or hashlib.sha256(text.encode()).hexdigest() != text_hash):
                    raise ValueError('Existing source page integrity failed; preserve it for inspection')
        db.execute('INSERT OR REPLACE INTO sources VALUES(?,?,?)',(source_id,sha,len(reader.pages)))
        db.execute('DELETE FROM passages WHERE source_id=?',(source_id,))
        for index,page in enumerate(reader.pages,1):
            text = re.sub(r'\s+',' ',page.extract_text() or '').strip()
            # Retain extraction status separately; no fabricated printed page.
            db.execute('INSERT OR IGNORE INTO pages VALUES(?,?,?,?,?)',
                       (source_id,index,text,hashlib.sha256(text.encode()).hexdigest(),'EXTRACTED_NOT_REVIEWED'))
            db.execute('INSERT INTO passages VALUES(?,?,?)',(source_id,index,text))
    return {'source_id':source_id,'sha256':sha,'pdf_pages':len(reader.pages),'status':'INDEXED_NOT_RULE_APPROVAL'}

def search(database_path, query, limit=8):
    if type(limit) is not int or not 1 <= limit <= 50: raise ValueError('limit must be between 1 and 50')
    tokens = re.findall(r'\w+',query,flags=re.UNICODE)
    if not tokens: return []
    # Parameters and escaped FTS tokens: query text is never SQL/instructions.
    match=' AND '.join('"'+token.replace('"','""')+'"' for token in tokens)
    uri = Path(database_path).resolve().as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as db:
        rows=db.execute('''SELECT p.source_id,p.pdf_page,p.text,p.text_sha256,p.review_status,s.sha256,f.text
            FROM passages f JOIN pages p ON p.source_id=f.source_id AND p.pdf_page=f.pdf_page
            JOIN sources s ON s.id=p.source_id WHERE passages MATCH ?
            ORDER BY bm25(passages),p.source_id,p.pdf_page LIMIT ?''',(match,limit)).fetchall()
    if any(hashlib.sha256(r[2].encode()).hexdigest()!=r[3] or r[6] != r[2] for r in rows):
        raise ValueError('Indexed passage integrity failed; rebuild from the immutable source')
    return [{'source_id':r[0],'pdf_page':r[1],'text':r[2],'passage_sha256':r[3],
             'review_status':r[4],'source_sha256':r[5],
             'use':'SOURCE_WITNESS_ONLY_NOT_APPROVED_INTERPRETATION'} for r in rows]
