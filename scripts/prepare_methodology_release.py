"""Prepare an exact committed release for the existing Astro project; never logs secrets."""
import json,subprocess,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
if subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():
    raise SystemExit('Commit all intended source changes before preparing an exact release')
archive=ROOT/'evidence/private/methodology-release.zip'
subprocess.run(['git','archive','--format=zip','--output',str(archive),commit],cwd=ROOT,check=True)
directory=Path(tempfile.mkdtemp(prefix='Mystic-Rebels-methodology-'))
with zipfile.ZipFile(archive) as package:package.extractall(directory)
(directory/'.vercel').mkdir()
(directory/'.vercel/project.json').write_text(json.dumps({'projectName':'mystic-rebels-chart-generator',
    'projectId':'prj_MBgBhgCUjxUwJ8OZO9OrqDqK4Vwl','orgId':'team_8iuNbs04mGL8bwcfLrYefuKD'}),encoding='utf-8')
record={'source_commit':commit,'directory':str(directory),'project_id':'prj_MBgBhgCUjxUwJ8OZO9OrqDqK4Vwl',
        'team_id':'team_8iuNbs04mGL8bwcfLrYefuKD','production_domain':'www.cosmodynamicschart.site',
        'status':'PREPARED_NOT_DEPLOYED'}
(ROOT/'evidence/private/methodology-release.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
