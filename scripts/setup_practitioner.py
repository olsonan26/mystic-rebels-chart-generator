"""Create private local credentials; run again with --rotate to invalidate sessions.

No packages or external services are used. The generated secret is written only
under ignored tmp, not printed in logs. Existing credentials are preserved.
"""
from pathlib import Path
import argparse
import hashlib
import json
import secrets
import sys

ROOT=Path(__file__).resolve().parents[1]


def setup(rotate=False, actor='Local practitioner'):
    directory=ROOT/'tmp/practitioner-private'
    directory.mkdir(parents=True,exist_ok=True,mode=0o700)
    path=directory/'config.json'
    if path.exists() and not rotate:
        return path
    password=secrets.token_urlsafe(24); salt=secrets.token_bytes(16)
    record='pbkdf2_sha256$240000$'+salt.hex()+'$'+hashlib.pbkdf2_hmac('sha256',password.encode(),salt,240000).hex()
    path.write_text(json.dumps({'NADIA_REVIEW_STORE':str(directory/'cases'),
        'NADIA_REVIEW_PASSWORD_HASH':record,'NADIA_REVIEWER_NAME':actor},indent=2),encoding='utf-8')
    (directory/'sign-in.txt').write_text(password+'\n',encoding='utf-8')
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rotate',action='store_true')
    parser.add_argument('--actor',default='Local practitioner')
    args=parser.parse_args()
    path=setup(args.rotate,args.actor)
    print('Private configuration: '+str(path))
    print('Read sign-in.txt in that private directory to sign in. Do not share or commit it.')
