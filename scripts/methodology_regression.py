"""Immutable pre-methodology snapshots; compare established point fields exactly."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'scripts'))
from mystic_rebels.models import BirthInput
from mystic_rebels.service import calculate
from wheel_regression import original_engine_cases, differences, across_environments

OUT = ROOT / 'evidence' / 'methodology-followup'
BASE = OUT / 'before.json'

def canonical(value):
    return {k: v for k, v in value.items() if k != 'created_at_utc'}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if '--record' in sys.argv:
        if BASE.exists():
            raise SystemExit('Refusing to overwrite immutable baseline')
        old = json.loads((ROOT / 'evidence/wheel-refinement/before.json').read_text(encoding='utf-8'))
        inputs = old['inputs']
        inputs += [{**inputs[0], 'name': 'Aries boundary epoch', 'local_date': '2024-03-20', 'local_time': '03:06:00', 'timezone': 'UTC'},
                   {**inputs[0], 'name': 'Polar geometry unavailable', 'latitude': 90}]
        result = {'baseline_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  'source_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'mystic_rebels').glob('*.py'))},
                  'inputs': inputs, 'charts': [canonical(calculate(BirthInput(**x))) for x in inputs]}
        BASE.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(f'Recorded {len(inputs)} complete charts before calculation changes')
        return
    before = json.loads(BASE.read_text(encoding='utf-8'))
    after = [canonical(calculate(BirthInput(**x))) for x in before['inputs']]
    # Execute the archived predecessor on this same Python/native runtime so
    # Linux CI does not conflate compiler/libm drift with a changed calculation.
    reference = original_engine_cases(before['baseline_commit'], before['inputs'], before['source_sha256'])
    changes = []
    established = 0
    for case, (old, new) in enumerate(zip(reference, after)):
        assert old['angles'] == new['angles']
        assert old['whole_sign_cusps'] == new['whole_sign_cusps']
        assert old['time'] == new['time']
        assert old['configuration'] == new['configuration']
        for left, right in zip(old['points'], new['points']):
            assert left['id'] == right['id']
            if left['available']:
                # Additive verification metadata is allowed; every old point field is fixed.
                assert all(right.get(k) == v for k, v in left.items()), (case, left['id'])
                established += 1
            elif left != right:
                changes.append({'case': case, 'id': left['id'], 'before_available': False, 'after_available': right['available']})
    result = {'baseline_commit': before['baseline_commit'], 'cases': len(after), 'established_points_exact': established,
              'angles_cusps_times_configuration_exact': True, 'newly_supported_points': changes,
              'same_runtime_archived_engine_comparison': True,
              'frozen_snapshot_cross_platform_differences': len(differences(across_environments(before['charts']), across_environments(reference))),
              'baseline_sha256': hashlib.sha256(BASE.read_bytes()).hexdigest()}
    (OUT/'regression.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
