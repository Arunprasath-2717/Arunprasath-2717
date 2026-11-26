import json, pathlib, re, tempfile, unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from io import BytesIO
import build_profile as p
import cinema

class ProfileTests(unittest.TestCase):
    def test_calendar_aggregation(self):
        payload={'data':{'user':{'contributionsCollection':{'contributionCalendar':{'weeks':[
            {'contributionDays':[{'date':'2026-11-22','contributionCount':3},{'date':'2026-11-23','contributionCount':5}]},
            {'contributionDays':[{'date':'2026-11-15','contributionCount':1}]}]}}}}}
        with patch.object(p.urllib.request,'urlopen',return_value=BytesIO(json.dumps(payload).encode())):
            self.assertEqual(p.fetch('test')['weeks'],[{'date':'2026-11-15','count':1},{'date':'2026-11-22','count':8}])
    def test_invalid_snapshot(self):
        with self.assertRaises(AssertionError):
            p.validate({'as_of':'2026-11-26','weeks':[{'date':'2026-11-22','count':-1}]})
    def test_render(self):
        profile=json.loads((p.DATA/'profile.json').read_text())
        data={'as_of':'2026-11-26','weeks':[{'date':'2026-11-15','count':0},{'date':'2026-11-22','count':9}]}
        with tempfile.TemporaryDirectory() as d, patch.object(cinema,'OUT',pathlib.Path(d)):
            for theme in cinema.THEMES:
                cinema.hero(theme)
                for i,project in enumerate(profile['projects'],1): cinema.project(theme,project,i)
                cinema.toolkit(theme);cinema.timeline(theme);cinema.activity(theme,data)
            files=list(pathlib.Path(d).glob('*.svg'))
            self.assertEqual(len(files),12)
            for f in files:
                s=f.read_text();root=ET.fromstring(s)
                self.assertEqual(root.attrib['role'],'img')
                self.assertIn('prefers-reduced-motion',s)
                for token in ('linearGradient','radialGradient','<script','<filter','foreignObject'):
                    self.assertNotIn(token,s)
                self.assertLess(len(s.encode()),50_000)
            s=(pathlib.Path(d)/'activity-dark.svg').read_text()
            self.assertIn('Week of 2026-11-22: 9 contributions',s)
    def test_readme_assets(self):
        md=(p.ROOT/'README.md').read_text()
        refs=set(re.findall(r'(?:src|srcset)="(assets/[^"]+)"',md))
        self.assertEqual(len(refs),12)
        for f in refs: ET.parse(p.ROOT/f)
        data=json.loads((p.DATA/'contributions.json').read_text())
        p.validate(data)
        for theme in cinema.THEMES:
            s=(p.ASSETS/f'activity-{theme}.svg').read_text()
            self.assertEqual(len(re.findall(r'<title>Week of ',s)),len(data['weeks']))
    def test_api_failure(self):
        with patch.object(p.urllib.request,'urlopen',return_value=BytesIO(b'{"errors":[{"message":"unavailable"}]}')):
            with self.assertRaises(ValueError): p.fetch('test')
    def test_motion(self):
        for name in ('identity','verifai','atlox','toolchain','activity'):
            s=(p.ASSETS/f'{name}-dark.svg').read_text()
            self.assertIn('@keyframes',s)
            self.assertIn('animation:',s)
if __name__=='__main__':unittest.main()
