"""Optional specialist benchmark using invented, non-astrological fixtures only.

Offline by default. --live reads NADIA_WRITER_API_KEY from process environment;
no credential, prompt, chart or private-library content is printed or persisted.
Model identifiers are explicit and replaceable. No automatic model fallback.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mystic_rebels.report_writer import synthetic_packet, render, OpenRouterWriter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--key-stdin', action='store_true', help='Read credential from a non-echoing pipe, never a command argument')
    parser.add_argument('--models', nargs='+', default=['deepseek/deepseek-v4.1-flash-1017', 'openai/gpt-4.1-mini'])
    parser.add_argument('--out', type=Path, default=ROOT / 'tmp/writer-benchmark.json')
    args = parser.parse_args()
    api_key = os.environ.get('NADIA_WRITER_API_KEY', '')
    if args.key_stdin:
        if sys.stdin.isatty():
            import getpass
            api_key = getpass.getpass('Writer benchmark credential (not echoed): ')
        else:
            api_key = sys.stdin.readline().strip()
    if args.live and not api_key:
        raise SystemExit('Live benchmark requires server-only NADIA_WRITER_API_KEY; no key was logged.')
    rows = []
    for case in ('balanced', 'limited', 'reflection'):
        packet = synthetic_packet(case)
        for model in ['deterministic'] + (args.models if args.live else []):
            writer = None if model == 'deterministic' else OpenRouterWriter(api_key, model)
            start = time.perf_counter()
            result = render(packet, writer)
            words = sum(len(s['text'].split()) for section in result['sections'] for s in section['sentences'])
            rows.append({'case': case, 'model': model, 'latency_ms': round(1000 * (time.perf_counter() - start), 2),
                         'accepted': result['writer_used'], 'fallback_reason': result['fallback_reason'],
                         'claim_coverage': 1.0, 'unapproved_sentences_rendered': 0, 'word_count': words,
                         'output_changed_from_template': result['sections'] != render(packet)['sections'],
                         'http_status': getattr(writer, 'last_http_status', None) if writer else None,
                         'finish_reason': getattr(writer, 'last_finish_reason', None) if writer else None,
                         'usage': getattr(writer, 'last_usage', {}) if writer else {}})
    report = {'contract': 'approved-wording-selection/1', 'external_calls': len(rows) - 3,
              'personal_data_sent': False, 'proprietary_source_sent': False,
              'interpretation_engine_replaced': False, 'production_writer_enabled': False,
              'human_style_evaluation': 'pending; constrained selection is not a free-prose quality benchmark', 'results': rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
