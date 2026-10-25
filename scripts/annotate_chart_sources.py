"""Attach cited vocabulary to supplied natal facts, without personal inference."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from knowledge_audit.report_components import usage_catalog,annotate_chart,render_markdown


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--format',choices=['json','markdown'],default='json')
    args=parser.parse_args()
    def load(name):return json.loads((ROOT/'data/knowledge'/name).read_text(encoding='utf-8'))
    catalog=usage_catalog(load('interpretive_inventory.json'),load('original_assertions.json'),load('source_blocker_findings.json'),load('source_meaning_profiles.json'))
    try:packet=annotate_chart(json.loads(args.input.read_text(encoding='utf-8')),catalog)
    except ValueError as error:parser.error(str(error))
    sys.stdout.write(render_markdown(packet) if args.format=='markdown' else json.dumps(packet,ensure_ascii=True,indent=2)+'\n')


if __name__=='__main__':main()
