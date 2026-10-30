"""Frozen, attributed source ingredients for the local research prototype."""
from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path

@lru_cache(maxsize=1)
def source_pack():
    return json.loads((Path(__file__).resolve().parent / 'data' / 'source-pack.json').read_text(encoding='utf-8'))

def source_catalog():
    return deepcopy(list(source_pack()['sources'].values()))

def source_record(source_id):
    return deepcopy(source_pack()['sources'][source_id])

def number_vocabulary(digit):
    return deepcopy(source_pack()['numbers'][str(digit)])

def role_vocabulary(role, digit):
    source_id = source_pack()['role_vocabularies'][role][str(digit)]
    return source_record(source_id)
