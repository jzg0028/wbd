import unittest

from Navigation.prod.util.Sighting import Sighting
import xml.etree.ElementTree as ET

class SightingTest(unittest.TestCase):

    def getSightings(self, root, sighting, star, aries):
        sighting = root + sighting
        star = root + star
        aries = root + aries

        return [Sighting(node, star, aries)
            for node in ET.parse(sighting).getroot()]
    
    def testToString(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'sightings.xml',
            'stars.txt',
            'aries.txt'
        )

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.1\t83d43.8",
            str(arr[0])
        )
        self.assertEqual (
            "Sirius\t2017-04-17\t09:30:30\t45d11.9\t-16d44.5\t247d6.2",
            str(arr[1])
        )

    def testGeographicLongitude(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'sightings.xml',
            'stars.txt',
            'aries.txt'
        )

        self.assertEqual('83d43.8', arr[0].geographicLongitude())
        self.assertEqual('247d6.2', arr[1].geographicLongitude())

    def testGeographicLatitude(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'sightings.xml',
            'stars.txt',
            'aries.txt'
        )

        self.assertEqual('27d59.1', arr[0].geographicLatitude())
        self.assertEqual('-16d44.5', arr[1].geographicLatitude())

    def testAdjustedAltitude(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'sightings.xml',
            'stars.txt',
            'aries.txt'
        )

        self.assertEqual('15d1.5', arr[0].adjustedAltitude())
        self.assertEqual('45d11.9', arr[1].adjustedAltitude())
