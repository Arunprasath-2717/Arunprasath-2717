import tempfile, unittest, xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
import render_profile as r

class RenderTests(unittest.TestCase):
    def test_static_and_sample(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(r,'ASSETS',Path(tmp)):
            r.hero(); r.pipeline(); r.stack(); r.projects(); r.contact()
            r.telemetry({'scope':'sample','as_of':'2026-11-26','repos':[{'name':'<escaped>','language':'Python','stargazers_count':2,'forks_count':0,'pushed_at':'2026-11-25'}], 'calendar':None})
            for file in Path(tmp).glob('*.svg'): ET.parse(file)
            self.assertEqual(len(list(Path(tmp).glob('*.svg'))),9)
            text=(Path(tmp)/'telemetry.svg').read_text()
            self.assertIn('INITIAL VERIFIED SAMPLE',text); self.assertIn('&lt;escaped&gt;',text); self.assertIn('CALENDAR AWAITING',text)
    def test_calendar(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(r,'ASSETS',Path(tmp)):
            r.telemetry({'scope':'public','as_of':'2026-11-26','repos':[], 'calendar':{'totalContributions':3,'weeks':[{'contributionDays':[{'date':'2026-11-26','contributionCount':3}]}]}})
            file=Path(tmp)/'telemetry.svg'; ET.parse(file)
            self.assertIn('3 contributions',file.read_text())
    def test_fetch_filters(self):
        with patch.object(r,'request',side_effect=[[{'name':'ok','language':'Python'},{'name':r.LOGIN},{'name':'private','private':True},{'name':'fork','fork':True}],{'errors':[{'message':'unavailable'}]}]):
            d=r.fetch_live(); self.assertEqual([x['name'] for x in d['repos']],['ok']); self.assertIsNone(d['calendar'])
if __name__=='__main__': unittest.main()
