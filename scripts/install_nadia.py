"""Install an owner-supplied private wheel after checking the immutable digest.

Acquire it from the private release with a scoped read credential outside this
script. No download credential, wheel or installed rules belong in public Git.
"""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nadia_runtime import SHA256, WHEEL, verified_core

def install(wheel):
    wheel = Path(wheel).resolve()
    if wheel.name != WHEEL or hashlib.sha256(wheel.read_bytes()).hexdigest() != SHA256:
        raise ValueError('Wheel does not match approved release')
    runtime = ROOT / '.nadia-private'
    runtime.mkdir(exist_ok=True)
    site = runtime / 'site'
    if site.exists():
        raise ValueError('Existing runtime retained; stage rollback in a fresh checkout')
    shutil.copyfile(wheel, runtime / WHEEL)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-index', '--no-deps',
                    '--no-compile', '--target', str(site), str(runtime / WHEEL)], check=True)
    verified_core(runtime)
    print('Verified private core 0.7.0; personal readings disabled')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('wheel')
    install(parser.parse_args().wheel)
