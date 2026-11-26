import base64, json, pathlib, re, tempfile, unittest
from io import BytesIO
from unittest.mock import patch
import xml.etree.ElementTree as ET
import build_profile as p
import cinema
import realm
NS={'s':'http://www.w3.org/2000/svg'}
XLINK='{http://www.w3.org/1999/xlink}href'
class ProfileTests(unittest.TestCase):
    def test_calendar_aggregation(self):
        data={'data':{'user':{'contributionsCollection':{'contributionCalendar':{'weeks':[{'contributionDays':[{'date':'2026-11-22','contributionCount':3},{'date':'2026-11-23','contributionCount':5}]},{'contributionDays':[{'date':'2026-11-15','contributionCount':1}]}]}}}}}
        with patch.object(p.urllib.request,'urlopen',return_value=BytesIO(json.dumps(data).encode())):
            self.assertEqual(p.fetch('test')['weeks'],[{'date':'2026-11-15','count':1},{'date':'2026-11-22','count':8}])
    def test_invalid_snapshot(self):
        with self.assertRaises(AssertionError):p.validate({'as_of':'2026-11-26','weeks':[{'date':'2026-11-22','count':-1}]})
    def test_api_failure(self):
        with patch.object(p.urllib.request,'urlopen',return_value=BytesIO(b'{"errors":[{"message":"unavailable"}]}')):
            with self.assertRaises(ValueError):p.fetch('test')
    def test_render(self):
        profile=json.loads((p.DATA/'profile.json').read_text());data={'as_of':'2026-11-26','weeks':[{'date':'2026-11-15','count':0},{'date':'2026-11-22','count':9}]}
        with tempfile.TemporaryDirectory() as d,patch.object(cinema,'OUT',pathlib.Path(d)):
            for theme in cinema.THEMES:
                for i,project in enumerate(profile['projects'],1):cinema.project(theme,project,i)
                realm.toolkit(theme);realm.focus(theme);realm.lifecycle(theme);cinema.activity(theme,data)
            files=list(pathlib.Path(d).glob('*.svg'));self.assertEqual(len(files),14)
            for f in files:
                s=f.read_text();root=ET.fromstring(s)
                self.assertEqual(root.attrib['role'],'img');self.assertIn('prefers-reduced-motion',s)
                for token in ('linearGradient','radialGradient','<script','<filter','foreignObject'):self.assertNotIn(token,s)
                self.assertLess(len(s.encode()),50_000)
            self.assertIn('Week of 2026-11-22: 9 contributions',(pathlib.Path(d)/'activity-dark.svg').read_text())
    def test_readme_assets(self):
        md=(p.ROOT/'README.md').read_text();refs=set(re.findall(r'(?:src|srcset)="(assets/[^"]+)"',md))
        self.assertEqual(len(refs),20)
        for f in refs:
            self.assertTrue((p.ROOT/f).is_file(),f)
            if f.endswith(".svg"):ET.parse(p.ROOT/f)
        for slug in ('VerifAI','VOILORACLE','CANE'):self.assertIn('https://github.com/Arunprasath-2717/'+slug,md)
    def test_real_data(self):
        data=json.loads((p.DATA/'contributions.json').read_text());p.validate(data)
        for theme in cinema.THEMES:
            s=(p.ASSETS/f'activity-{theme}.svg').read_text();self.assertEqual(len(re.findall(r'<title>Week of ',s)),len(data['weeks']))
            for w in data['weeks']:self.assertIn(f'Week of {w["date"]}: {w["count"]} contributions',s)
    def test_cinematic_assets(self):
        for name,plate,view,limit in [('ruins-hero.svg','ruins-landscape.webp','0 0 1600 640',1_000_000),('river-hero.svg','river-landscape.webp','0 0 1440 640',500_000)]:
            s=(p.ASSETS/name).read_text();root=ET.fromstring(s)
            self.assertEqual(root.attrib['viewBox'],view);self.assertIn('prefers-reduced-motion',s);self.assertIn('@keyframes water',s);self.assertIn('@keyframes mote',s);self.assertNotIn('@keyframes camera',s);self.assertNotIn('<script',s);self.assertNotIn('foreignObject',s)
            uris=[i.attrib[XLINK] for i in root.findall('.//s:image',NS)]
            self.assertTrue(all(x.startswith('data:image/') for x in uris));self.assertIn((p.ASSETS/plate).read_bytes(),[base64.b64decode(x.split(',',1)[1]) for x in uris]);self.assertLess(len(s.encode()),limit)
            self.assertTrue(root.findall('.//s:mask',NS))
        self.assertNotIn('animation:',(p.ASSETS/'ruins-still.svg').read_text())
        root=ET.parse(p.ASSETS/'ruins-hero.svg').getroot();name=[t for t in root.findall('.//s:text',NS) if t.text=='Arun Prasath'];self.assertEqual(len(name),1);self.assertEqual(name[0].attrib['text-anchor'],'middle')
    def test_motion(self):
        for theme in cinema.THEMES:
            for name in ('verifai','atlox','cane','toolchain','focus','lifecycle'):
                s=(p.ASSETS/f'{name}-{theme}.svg').read_text();self.assertIn('@keyframes',s);self.assertIn('animation:',s)
if __name__=='__main__':unittest.main()
