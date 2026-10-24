import swisseph as swe
import json
from pathlib import Path

def entry(id,name,glyph,group,body=None,**extra):return dict(id=id,name=name,glyph=glyph,group=group,body=body,**extra)

CATALOG=[entry(name,name,glyph,'Planets',getattr(swe,name.upper())) for name,glyph in zip(['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto'],'☉☽☿♀♂♃♄♅♆♇')]
CATALOG += [entry(name,name,glyph,'Asteroids',getattr(swe,name.upper()),assets=['seas_18.se1']) for name,glyph in [('Chiron','⚷'),('Ceres','⚳'),('Pallas','⚴'),('Juno','⚵'),('Vesta','⚶')]]
for number,name in json.loads((Path(__file__).resolve().parents[1]/'data'/'minor-bodies.json').read_text()):
    stem=f'se{number:05d}' if number<100000 else f's{number:06d}'
    CATALOG.append(entry(name,name,str(number),'Minor bodies',swe.AST_OFFSET+number,assets=[f'ast{number//1000}/{stem}s.se1'],number=number,max_year=2099))
CATALOG += [entry('NorthNodeTrue','North Node · true','☊','Lunar points',swe.TRUE_NODE),entry('NorthNodeMean','North Node · mean','☊','Lunar points',swe.MEAN_NODE),entry('SouthNodeTrue','South Node · true','☋','Lunar points'),entry('SouthNodeMean','South Node · mean','☋','Lunar points'),entry('LilithMean','Black Moon Lilith · mean','⚸','Lunar points',swe.MEAN_APOG),entry('LilithTrue','Black Moon Lilith · osculating','⚸','Lunar points',swe.OSCU_APOG),entry('SophiaMean','White Moon Sophia · mean','Wm','Lunar points',available=False,reason='The mean-perigee calculation needs final method verification.'),entry('SophiaTrue','White Moon Sophia · osculating','Wt','Lunar points',available=False,reason='The osculating-perigee calculation needs final method verification.')]
CATALOG += [entry(id,name,glyph,'Angles') for id,name,glyph in [('Ascendant','Ascendant','AC'),('Descendant','Descendant','DC'),('Midheaven','Midheaven','MC'),('ImumCoeli','Imum Coeli','IC'),('Vertex','Vertex','Vx'),('Invertex','Invertex','Av'),('Nonagesimal','Nonagesimal','No'),('Subnonagesimal','Subnonagesimal','Sn')]]
CATALOG += [entry(id,name,glyph,'Parts') for id,name,glyph in [('Fortune','Part of Fortune','⊗'),('Spirit','Part of Spirit','⊙'),('Love','Part of Love','♡')]]
BY_ID={row['id']:row for row in CATALOG}
PRESETS={'Basic':[r['id'] for r in CATALOG if r['group']=='Planets']+['Ascendant','Midheaven'],'Expanded':[r['id'] for r in CATALOG if r['group'] in ('Planets','Asteroids')]+['NorthNodeTrue','SouthNodeTrue','LilithMean','Ascendant','Descendant','Midheaven','ImumCoeli','Vertex','Fortune','Spirit','Love']}
