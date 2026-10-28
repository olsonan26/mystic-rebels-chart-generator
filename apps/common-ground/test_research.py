"""Regression checks for method boundaries and the real calculate/render packet."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).parent))
from fastapi.testclient import TestClient
from app import app
from annual_adapter import annual_numbers
from phsr import ORDER,assess

HERE=Path(__file__).parent
client=TestClient(app)

def case(**changes):
    return dict(full_name='Nadia Sanchez',birth_date='1992-07-17',birth_time='20:01',
                time_accuracy='nearest_minute',latitude=33.8044,longitude=-118.0673,
                timezone='America/Los_Angeles',location_name='Los Alamitos',year=2011,**changes)

class ResearchChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        response=client.post('/api/research',json=case())
        assert response.status_code==200,response.text
        cls.result=response.json()

    def test_full_ruler_route_and_cycle(self):
        route=self.result['assessment']['root_route']
        self.assertEqual(route['path'],['Chiron','Sun','Moon','Neptune','Saturn','Uranus'])
        self.assertEqual(route['cycle'],['Saturn','Uranus'])
        self.assertEqual(route['repeat'],'Saturn')

    def test_stages_motion_occupants_and_conflicts(self):
        nodes=self.result['assessment']['assessments']
        for node in nodes.values():self.assertEqual([s['stage'] for s in node['stages']],ORDER)
        self.assertEqual(nodes['Chiron']['house'],8)
        self.assertEqual(nodes['Sun']['house'],7)
        self.assertEqual(nodes['Chiron']['stages'][0]['motion'],'direct')
        self.assertEqual(nodes['Chiron']['stages'][3]['pulse'],'Sagittarius')
        self.assertEqual(nodes['Chiron']['stages'][3]['associated_planet'],'Jupiter')
        self.assertIsNone(nodes['Chiron']['stages'][2]['canonical_spark'])
        self.assertEqual(nodes['Moon']['stages'][0]['motion'],'direct')
        self.assertTrue(nodes['Moon']['stages'][1]['delegate_retrograde'])
        self.assertEqual(nodes['Chiron']['stages'][4]['directed_aspects'],[])
        sun_occupants={p['id'] for p in nodes['Sun']['delegate_payload']['occupants']}
        self.assertTrue({'Chiron','Mercury','Venus','Vertex'}<=sun_occupants)
        self.assertFalse(self.result['reported_history_used'])

    def test_2011_compounds_and_months(self):
        a=self.result['annual'];f=a['fields']
        self.assertEqual(f['ess']['trail'],[14,5]);self.assertEqual(f['py']['trail'],[28,10,1])
        self.assertEqual(f['com']['trail'],[42,6]);self.assertEqual(f['com']['meaning']['number'],42)
        july=a['months'][6];self.assertEqual(july['pme']['trail'],[13,4])
        self.assertEqual(july['indicator']['tone'],'red')

    def test_2013_com_does_not_repaint_july(self):
        a=annual_numbers('Nadia Sanchez','1992-07-17',2013)
        self.assertEqual(a['fields']['com']['trail'],[49,13,4])
        self.assertTrue(a['fields']['com']['alert']['active'])
        self.assertEqual(a['months'][6]['indicator']['tone'],'yellow')

    def test_unknown_time_withholds_house_reading(self):
        data=case();data.update(birth_time=None,time_accuracy='unknown')
        response=client.post('/api/research',json=data)
        self.assertEqual(response.status_code,200,response.text)
        result=response.json()
        self.assertIsNone(result['assessment']['assessments']['Chiron']['house'])
        self.assertIn('withheld',result['reading']['paragraphs'][0])

    def test_invalid_year_or_policy_rejected_without_false_result(self):
        data=case();data['year']=1991
        self.assertEqual(client.post('/api/research',json=data).status_code,422)
        data=case();data['annual_name_policy']='married'
        self.assertEqual(client.post('/api/research',json=data).status_code,422)
        data=case();data['year']=2011.5
        self.assertEqual(client.post('/api/research',json=data).status_code,422)

if __name__=='__main__':unittest.main(verbosity=2)
