import unittest

from Navigation.prod.util.Sighting import Sighting
import xml.etree.ElementTree as ET
from Navigation.prod.util.Coordinate import Coordinate

class SightingTest(unittest.TestCase):

    def getSightings(self, root, sighting, star, aries, lat, lon):
        sighting = root + sighting
        star = root + star
        aries = root + aries

        return [Sighting(node, star, aries, Coordinate(lat, lon))
            for node in ET.parse(sighting).getroot()]
    
    def testToString(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'pollux.xml',
            'stars.txt',
            'aries.txt',
            'S53d38.4',
            '74d35.3'
        )

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.1\t" \
            + "84d33.4\tN27d59.5\t85d33.4\t292d44.6\t174",
            str(arr[0])
        )

    def testGeographicLongitude(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'pollux.xml',
            'stars.txt',
            'aries.txt'
            'S53d38.4',
            '74d35.3'
        )

        self.assertEqual('84d33.4', arr[0].geographicPosition
            .longitude().getString())

    def testGeographicLatitude(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'pollux.xml',
            'stars.txt',
            'aries.txt'
            'S53d38.4',
            '74d35.3'
        )

        self.assertEqual('27d59.1', arr[0].geographicPosition
            .latitude().getString())

    def testAdjustedAltitude(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'pollux.xml',
            'stars.txt',
            'aries.txt'
            'S53d38.4',
            '74d35.3'
        )

        self.assertEqual('15d1.5', arr[0].adjustment.altitude().getString())
