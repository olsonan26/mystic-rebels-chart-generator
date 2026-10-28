"""Extract a small, attributed research ingredient pack; never rewrites source repos."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
MYSTIC = HERE.parent / 'Mystic-Rebels'
COSTAR = WORKSPACE / 'reports' / 'mystic-costar-analysis-20261027' / 'evidence' / 'LOOKS-LIKE-COSTAR'
MYSTIC_SHA = '3d83db75c30b26d9b068576d84ec49554822fd8c'
COSTAR_SHA = '023140de4ac9ebad8a804b4c984337135e77b19a'

def read(path):
    return path.read_text(encoding='utf-8-sig')

def make_pack():
    inventory_path = MYSTIC / 'data' / 'knowledge' / 'interpretive_inventory.json'
    profiles_path = MYSTIC / 'data' / 'knowledge' / 'source_meaning_profiles.json'
    inventory = json.loads(read(inventory_path))
    profiles = json.loads(read(profiles_path))
    records = {}
    for row in inventory['records']:
        if re.fullmatch(r'meaning-(sun|moon|mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto)|field-\d\d|objective-context|tone-pulse|house-field|phsr', row['id']):
            records['mr:' + row['id']] = {
                'id': 'mr:' + row['id'], 'system': 'Mystic Rebels', 'title': row['title'],
                'statement': row['meaning_summary'], 'source_status': row['source_status'],
                'answer_use': row.get('answer_use'), 'exceptions': row.get('exceptions', []),
                'witnesses': row.get('witnesses', []),
                'url': f'https://github.com/olsonan26/mystic-rebels-chart-generator/blob/{MYSTIC_SHA}/data/knowledge/interpretive_inventory.json',
                'record_id': row['id'], 'usage': 'Attributed component vocabulary in a research comparison; not approved personal-report synthesis.',
            }
    for row in profiles['profiles']:
        if row['kind'] != 'sign':
            continue
        records['mr:' + row['id']] = {
            'id': 'mr:' + row['id'], 'system': 'Mystic Rebels', 'title': row['title'],
            'statement': row['source_meaning'], 'source_status': row['vocabulary_status'],
            'witnesses': row['citations'], 'context_witnesses': row.get('context_citations', []),
            'url': f'https://github.com/olsonan26/mystic-rebels-chart-generator/blob/{MYSTIC_SHA}/data/knowledge/source_meaning_profiles.json',
            'record_id': row['id'], 'usage': 'Contextual expression style only; not a complete personality description.',
        }

    number_path = COSTAR / 'services' / 'pmeiEngine.ts'
    number_text = read(number_path)
    numbers = {}
    for match in re.finditer(r"^\s*([1-9]): \{ essence: '([^']+)', strengths: '([^']+)', watchouts: '([^']+)' \}", number_text, re.M):
        digit = int(match[1])
        numbers[str(digit)] = {'essence': match[2], 'strengths': match[3], 'watchouts': match[4]}
        records[f'costar-number-{digit}'] = {
            'id': f'costar-number-{digit}', 'system': 'LOOKS-LIKE-COSTAR',
            'title': f'Number {digit} vocabulary', 'statement': match[2] + '. Strengths in this bank: ' + match[3] + '.',
            'source_status': 'REPOSITORY_AUTHORED_VOCABULARY',
            'url': f'https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_SHA}/services/pmeiEngine.ts#L{number_text[:match.start()].count(chr(10)) + 1}',
            'usage': 'Authored symbolic vocabulary, not an observation established about a person.',
        }
    if len(numbers) != 9:
        raise ValueError('All nine number definitions must be extracted from the source.')

    direction_path = COSTAR / 'name-engine' / 'data' / 'numbers.ts'
    direction_text = read(direction_path)
    for bank_name in ('first_name_total_flavor', 'called_name_vibe', 'full_name_direction'):
        body = re.search(r'"' + bank_name + r'"\s*:\s*\{([^}]+)\}', direction_text).group(1)
        for match in re.finditer(r'"([1-9])"\s*:\s*("(?:\\.|[^"\\])*")', body):
            digit = int(match[1])
            source_id = f'costar-{bank_name}-{digit}'
            records[source_id] = {
                'id': source_id, 'system': 'LOOKS-LIKE-COSTAR',
                'title': f'{bank_name.replace("_", " ").title()} {digit}',
                'statement': json.loads(match[2]), 'source_status': 'REPOSITORY_AUTHORED_VOCABULARY',
                'url': f'https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_SHA}/name-engine/data/numbers.ts',
                'usage': 'This is the attributed bank\'s wording, not an independently observed personal fact. The separate name-cue engine has its own calculation conventions.',
            }

    records['costar-natal-calculations'] = {
        'id': 'costar-natal-calculations', 'system': 'LOOKS-LIKE-COSTAR', 'title': 'Natal calculation methods and roles',
        'statement': 'Expression uses full-name letter values; Soul Urge uses vowels; Birth Force uses birth-date digits; Ultimate Goal combines a reduced birthday component and Expression; Balance uses initials; Called Name combines reduced first and last names.',
        'source_status': 'SOURCE_CODE_METHOD',
        'url': f'https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_SHA}/services/numerology.ts#L254-L391',
    }
    records['costar-pmei'] = {
        'id': 'costar-pmei', 'system': 'LOOKS-LIKE-COSTAR', 'title': 'PMEI literal letter counts',
        'statement': 'Physical={4,5}; Mental={1,8}; Emotional={2,3,6}; Intuitive={7,9}. Every letter contributes one count. Counts are not digit-reduced. Zero planes are described as an all-or-nothing switch, not an absent human capacity.',
        'source_status': 'SOURCE_CODE_METHOD_AND_AUTHORED_VOCABULARY',
        'url': f'https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_SHA}/services/pmeiEngine.ts#L5-L47',
    }

    # Preserve the distinct banks actually selected by getCoreNumberDescription.
    # Ultimate Goal deliberately retains the existing lifePathDescriptions lookup;
    # this is not a claim that its calculation is a date-only Life Path.
    natal_path = COSTAR / 'services' / 'data.ts'
    natal_text = read(natal_path)
    banks = {
        'Soul Urge': 'soulUrgeDescriptions', 'Expression': 'expressionDescriptions',
        'Ultimate Goal': 'lifePathDescriptions', 'Birth Force': 'birthForceDescriptions',
        'Balance Number': 'balanceNumberDescriptions',
    }
    role_vocabularies = {}
    quoted = r'"(?:\\.|[^"\\])*"'
    for role, bank_name in banks.items():
        bank = re.search(r'export const ' + bank_name + r'[^=]*=\s*\{(?P<body>[\s\S]*?)\n\};', natal_text)
        if not bank:
            raise ValueError(f'Missing natal role bank: {bank_name}')
        role_vocabularies[role] = {}
        for row in re.finditer(r'^\s*"?([1-9])"?\s*:\s*(.+)$', bank['body'], re.M):
            digit = int(row[1])
            value = row[2]
            text_match = re.search(r'description:\s*(' + quoted + ')', value) if value.startswith('{') else re.match(quoted, value)
            if not text_match:
                raise ValueError(f'Missing meaning in {bank_name}: {digit}')
            meaning = json.loads(text_match[1] if value.startswith('{') else text_match[0])
            source_id = 'costar-role-' + role.lower().replace(' ', '-') + '-' + str(digit)
            line = natal_text[:bank.start('body') + row.start()].count('\n') + 1
            records[source_id] = {
                'id': source_id, 'system': 'LOOKS-LIKE-COSTAR', 'title': f'{role} {digit}: role-specific bank',
                'role': role, 'number': digit, 'bank': bank_name, 'statement': meaning,
                'source_status': 'REPOSITORY_AUTHORED_ROLE_VOCABULARY',
                'url': f'https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_SHA}/services/data.ts#L{line}',
                'usage': 'Attributed source wording, not an observed personal fact. The prototype compares the role without asserting this description is true of the person.',
            }
            if role == 'Ultimate Goal':
                records[source_id]['method_note'] = 'The calculator labels the feature Ultimate Goal and selects this bank, whose original wording says Life Path. The name-plus-date formula is preserved separately.'
            role_vocabularies[role][str(digit)] = source_id
        if len(role_vocabularies[role]) != 9:
            raise ValueError(f'Incomplete natal role bank: {bank_name}')

    called_path = COSTAR / 'services' / 'calledNameDescriptions.ts'
    called_text = read(called_path)
    role_vocabularies['Called Name'] = {}
    for row in re.finditer(r'number:\s*([1-9]),[\s\S]*?\bfull:\s*(' + quoted + ')', called_text):
        digit = int(row[1])
        source_id = f'costar-role-called-name-{digit}'
        records[source_id] = {
            'id': source_id, 'system': 'LOOKS-LIKE-COSTAR', 'title': f'Called Name {digit}: role-specific bank',
            'role': 'Called Name', 'number': digit, 'bank': 'calledNameDescriptions',
            'statement': json.loads(row[2]), 'source_status': 'REPOSITORY_AUTHORED_ROLE_VOCABULARY',
            'url': f'https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_SHA}/services/calledNameDescriptions.ts#L{called_text[:row.start()].count(chr(10)) + 1}',
            'usage': 'Attributed social-perception vocabulary, not evidence of what anyone actually thinks of this person.',
        }
        role_vocabularies['Called Name'][str(digit)] = source_id
    if len(role_vocabularies['Called Name']) != 9:
        raise ValueError('Incomplete called-name role bank.')
    records['bridge-method-v1'] = {
        'id': 'bridge-method-v1', 'system': 'New comparison proposal', 'title': 'Contextual correspondence method, version 1',
        'statement': 'Compare a number in its specific role with a selected planetary function and that planet\'s actual house, Tone and Pulse. A shared label is a proposed thematic link, not a physical aspect or independently validated association. No match count or strength score is calculated.',
        'source_status': 'ANALYST_PROPOSED_NOT_SOURCE_RULE', 'url': None,
        'usage': 'Research comparison only; the full PURE contextual interpretation and personal-report gates remain unchanged.',
    }
    records['mr:placements'] = {
        'id': 'mr:placements', 'system': 'Mystic Rebels', 'title': 'Whole Sign Field, Tone and Pulse calculation',
        'statement': 'House/True Placement follows Whole Sign house number; actual astronomical sign supplies Tone; same-element decan supplies Pulse. Degree is geometric position; Spark is unavailable.',
        'source_status': 'SOURCE_CODE_METHOD',
        'url': f'https://github.com/olsonan26/mystic-rebels-chart-generator/blob/{MYSTIC_SHA}/mystic_rebels/placements.py#L9-L15',
    }
    inputs = [inventory_path, profiles_path, number_path, direction_path, natal_path, called_path]
    return {
        'schema_version': '1.0', 'comparison_method': 'natal-contextual-bridge-v1',
        'generic_library_fallback_allowed': False, 'personal_report_approved': False,
        'source_commits': {'mystic_rebels': MYSTIC_SHA, 'looks_like_costar': COSTAR_SHA},
        'input_sha256': {str(p.relative_to(WORKSPACE)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        'sources': records, 'numbers': numbers, 'role_vocabularies': role_vocabularies,
    }

if __name__ == '__main__':
    path = HERE / 'data' / 'source-pack.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(make_pack(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Extracted attributed source pack.')
