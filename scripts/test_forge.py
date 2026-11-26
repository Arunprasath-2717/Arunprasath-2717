import unittest
import xml.etree.ElementTree as ET
import forge
class ForgeTests(unittest.TestCase):
    def test_data(self):
        cal={'weeks':[{'contributionDays':[{'date':'2026-11-22','contributionCount':2},{'date':'2026-11-23','contributionCount':5}]}]}
        self.assertEqual(forge.weekly(cal),[('2026-11-22',7)])
    def test_art_direction(self):
        svg=forge.render([('2026-11-22',7)],'2026-11-26')
        ET.fromstring(svg)
        for forbidden in ('linearGradient','radialGradient','<filter','<script','foreignObject'):
            self.assertNotIn(forbidden,svg)
        self.assertIn('7 contributions',svg)
        self.assertIn('prefers-reduced-motion',svg)
        self.assertIn('Week of 2026-11-22: 7 contributions',svg)
        self.assertLess(len(svg.encode()),40_000)
    def test_missing_calendar(self):
        self.assertIn('Contribution calendar unavailable',forge.render([],'2026-11-26'))
