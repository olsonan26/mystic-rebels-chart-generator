"""Reject private runtime files in Git or static browser artifacts."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
tracked = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
for name in tracked:
    if '.nadia-private' in Path(name).parts or name.endswith('.whl') or 'nadia_core' in Path(name).parts:
        raise ValueError('Private package tracked in public Git')
for base in (ROOT / 'web', ROOT / 'dist'):
    for path in base.rglob('*'):
        if not path.is_file() or 'node_modules' in path.parts:
            continue
        content = path.read_bytes()
        for marker in (b'nadia_core', b'.nadia-private', b'NADIA_HEALTH_TOKEN', b'nadia_knowledge_core'):
            if marker in content:
                raise ValueError('Private runtime reference in browser artifact')
        if path.suffix in {'.whl', '.py', '.pyc'}:
            raise ValueError('Server artifact in browser output')
print('Private package/browser boundary passed')
