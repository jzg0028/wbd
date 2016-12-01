import unittest

from Navigation.prod.util.Sighting import Sighting
import xml.etree.ElementTree as ET
from Navigation.prod.util.Coordinate import Coordinate
from Navigation.prod.util.Aries import Aries
from Navigation.prod.util.Star import Star

class SightingTest(unittest.TestCase):

    def getSightings(self, root, sighting, star, aries, lat, lon):
        sighting = root + sighting
        star = root + star
        aries = root + aries

        return [Sighting(node, star, aries, Coordinate(lat, lon))
            for node in ET.parse(sighting).getroot()]
    
    def testPollux(self):
        arr = self.getSightings (
            'SoftwareProcess/Navigation/resources/',
            'pollux.xml',
            'stars.txt',
            'aries.txt',
            'N27d59.5',
            '85d33.4'
        )

        

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.5\t" \
            + "84d33.4\tN27d59.5\t85d33.4\t7d21.1\t-2919",
            str(arr[0])
        )
