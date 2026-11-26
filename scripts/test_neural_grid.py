import tempfile, unittest, xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
import neural_grid as g
class NeuralGridTests(unittest.TestCase):
    def test_weekly(self):
        data={'calendar':{'weeks':[{'contributionDays':[{'date':'2026-11-22','contributionCount':2},{'date':'2026-11-23','contributionCount':5}]}]}}
        self.assertEqual(g.weekly(data),[('2026-11-22',7)])
        self.assertEqual(g.weekly({'calendar':None}),[])
    def test_render(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(g.r,'ASSETS',Path(tmp)):
            data={'as_of':'2026-11-26','calendar':{'weeks':[{'contributionDays':[{'date':'2026-11-22','contributionCount':7}]}]}}
            g.render(data)
            files=list(Path(tmp).glob('*.svg'))
            self.assertEqual(len(files),7)
            for f in files: ET.parse(f)
            city=Path(tmp,'neural-grid.svg').read_text()
            self.assertIn('7 CONTRIBUTIONS',city)
            self.assertIn('Week of 2026-11-22: 7 contributions',city)
            self.assertIn('prefers-reduced-motion',city)
            g.city({'as_of':'2026-11-26','calendar':None})
            self.assertIn('NO SYNTHETIC COUNTS',Path(tmp,'neural-grid.svg').read_text())
