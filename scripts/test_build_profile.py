import pathlib
import re
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from io import BytesIO
import json
import build_profile as p

class ArtworkTests(unittest.TestCase):
    def test_data_and_xml(self):
        weeks=[('2026-11-15',0),('2026-11-22',9)]
        svg=p.render(weeks,'2026-11-26')
        root=ET.fromstring(svg)
        self.assertEqual(root.attrib['viewBox'],'0 0 960 508')
        self.assertIn('9 contributions / 2 weeks',svg)
        self.assertIn('Week of 2026-11-15: 0 contributions',svg)
        self.assertIn('Week of 2026-11-22: 9 contributions',svg)
        self.assertIn('prefers-reduced-motion',svg)
        for forbidden in ('linearGradient','radialGradient','<filter','<script','foreignObject','http://www.w3.org/1999/xlink'):
            self.assertNotIn(forbidden,svg)
        self.assertLess(len(svg.encode()),40_000)

    def test_missing_data(self):
        svg=p.render([],'2026-11-26')
        self.assertIn('Calendar unavailable',svg)
        self.assertNotIn('contributions /',svg)

    def test_api_aggregation(self):
        payload={'data':{'user':{'contributionsCollection':{'contributionCalendar':{'weeks':[
            {'contributionDays':[{'date':'2026-11-22','contributionCount':3},{'date':'2026-11-23','contributionCount':5}]},
            {'contributionDays':[{'date':'2026-11-15','contributionCount':1}]}]}}}}}
        with patch.object(p.urllib.request,'urlopen',return_value=BytesIO(json.dumps(payload).encode())):
            self.assertEqual(p.calendar('test'),[('2026-11-15',1),('2026-11-22',8)])

    def test_published_asset_and_readme(self):
        svg=p.ASSET.read_text()
        ET.fromstring(svg)
        self.assertEqual(len(re.findall(r'<title>Week of ',svg)),53)
        readme=(p.ROOT/'README.md').read_text()
        self.assertIn('assets/workshop.svg',readme)
        self.assertEqual(len(re.findall(r'^\*\*\[',readme,re.M)),2)
        for asset in re.findall(r'src="(assets/[^"]+)"',readme):
            self.assertTrue((p.ROOT/asset).exists())

if __name__=='__main__': unittest.main()
