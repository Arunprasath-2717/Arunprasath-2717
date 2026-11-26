import base64, json, pathlib, re, tempfile, unittest
from io import BytesIO
from unittest.mock import patch
import xml.etree.ElementTree as ET
import build_profile as p
import cinema
import spectrum
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
        with tempfile.TemporaryDirectory() as d,patch.object(cinema,'OUT',pathlib.Path(d)),patch.object(spectrum,'OUT',pathlib.Path(d)):
            spectrum.build(data)
            for theme in cinema.THEMES:cinema.activity(theme,data)
            files=list(pathlib.Path(d).glob('*.svg'));self.assertEqual(len(files),13)
            for f in files:
                svg=f.read_text();root=ET.fromstring(svg)
                self.assertEqual(root.attrib['role'],'img')
                self.assertIn('prefers-reduced-motion',svg)
                self.assertNotIn('<script',svg)
                self.assertNotIn('foreignObject',svg)
            self.assertIn('Week of 2026-11-22: 9 contributions',(pathlib.Path(d)/'activity-dark.svg').read_text())
    def test_readme_assets(self):
        md=(p.ROOT/'README.md').read_text();refs=set(re.findall(r'(?:src|srcset)="(assets/[^"]+)"',md))
        self.assertEqual(len(refs),16)
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
        asset=(p.ASSETS/'reliable-systems-hero.webp').read_bytes()
        self.assertEqual(asset[:4],b'RIFF')
        self.assertEqual(asset[8:12],b'WEBP')
        self.assertEqual(int.from_bytes(asset[4:8],'little')+8,len(asset))
        self.assertLess(len(asset),1000000)
        self.assertIn('assets/reliable-systems-hero.webp',(p.ROOT/'README.md').read_text())
    def test_motion(self):
        for name in ('spectrum-cane.svg','spectrum-verifai.svg','spectrum-atlox.svg'):
            svg=(p.ASSETS/name).read_text()
            self.assertIn('@keyframes',svg)
            self.assertIn('animation:',svg)
        data=json.loads((p.DATA/'cane-routing.json').read_text())
        self.assertEqual(data['counts'],{'notify':18,'digest':37,'mute':55})
        self.assertEqual(sum(data['counts'].values()),110)
if __name__=='__main__':unittest.main()
