"""Inspect actual Chromium-exported PDFs, without uploading private report text.

Requires PyMuPDF for page/vector/text bounds and Pillow for contact sheets.
Run after verify_profile_browser.cjs. All outputs remain in ignored tmp.
"""
import hashlib
import json
from pathlib import Path
import re
import unicodedata

import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tmp/profile-browser'


def normalized(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))


def inspect(filename, packet_name, appendix=False):
    path = BASE / filename
    packet = json.loads((BASE / packet_name).read_text(encoding='utf-8'))
    document = fitz.open(path)
    pages, tiles, texts = [], [], []
    for index, page in enumerate(document):
        text = page.get_text()
        if len(text.strip()) < 40:
            raise ValueError('Blank or near-blank PDF page: ' + str(index + 1))
        for block in page.get_text('blocks'):
            if block[4].strip() and not (-1 <= block[0] <= block[2] <= page.rect.width + 1
                                         and -1 <= block[1] <= block[3] <= page.rect.height + 1):
                raise ValueError('Text outside page bounds: ' + str(index + 1))
        pix = page.get_pixmap(matrix=fitz.Matrix(.75, .75))
        image = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        image.thumbnail((300, 430))
        tile = Image.new('RGB', (320, 465), '#ddd')
        tile.paste(image, (10, 25))
        ImageDraw.Draw(tile).text((10, 6), str(index + 1), fill='black')
        tiles.append(tile)
        texts.append(text)
        pages.append({'page': index + 1, 'characters': len(text),
                      'vector_drawings': len(page.get_drawings()), 'text_within_page': True})
    combined = '\n'.join(texts)
    if 'PRIVATE_REFLECTION_TEST_NOT_FOR_EXPORT' in combined:
        raise ValueError('Private reflection leaked into PDF')
    if normalized(packet['profile']['name']) not in normalized(combined):
        raise ValueError('Profile name missing or clipped')
    if normalized('Personal conclusions require qualified review') not in normalized(combined):
        raise ValueError('Personal interpretation review boundary is missing')
    for section in packet['sections']:
        present = normalized(section['title']) in normalized(combined)
        expected = appendix and section['status'] in ('calculated', 'source_context')
        if present != expected:
            raise ValueError('Unexpected section visibility: ' + section['id'])
    if not any(p['vector_drawings'] > 300 for p in pages):
        raise ValueError('Vector chart not present')
    sheet = Image.new('RGB', (1280, ((len(tiles) + 3) // 4) * 465), '#aaa')
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % 4) * 320, (i // 4) * 465))
    sheet.save(BASE / (filename + '.png'))
    document[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(BASE / (filename + '.cover.png'))
    return {'filename': filename, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size, 'page_count': len(document), 'pages': pages,
            'intended_section_visibility_verified': True, 'appendix_included': appendix, 'complete_name_present': True,
            'reflection_absent': True, 'vector_chart_present': True,
            'visual_review': 'Contact sheets and full-resolution representative pages require separate visual inspection.'}


def main():
    import argparse
    global BASE
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', action='store_true', help='Inspect the private real-chart demonstration exports.')
    args = parser.parse_args()
    if args.product:
        BASE = ROOT / 'tmp/profile-product'
        results = [inspect('NADIA-Profile.pdf', 'profile.json'),
                   inspect('NADIA-Profile-with-evidence.pdf', 'profile.json', appendix=True)]
    else:
        results = [inspect('nadia-synthetic-profile.pdf', 'desktop.json'),
                   inspect('nadia-supporting-appendix.pdf', 'desktop.json', appendix=True),
                   inspect('nadia-unknown-time-long-name.pdf', 'unknown-time.json')]
    (BASE / 'pdf-inspection.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results))


if __name__ == '__main__':
    main()
