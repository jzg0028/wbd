import unittest

from Navigation.prod.util.Sighting import Sighting
import xml.etree.ElementTree as ET
from Navigation.prod.util.Coordinate import Coordinate
from Navigation.prod.util.Aries import Aries
from Navigation.prod.util.Star import Star

class SightingTest(unittest.TestCase):

    def getSightings(self, sighting, star, aries, lat, lon):
        return [Sighting(node, star, aries, Coordinate(lat, lon))
            for node in ET.parse(sighting).getroot()]
    
    def testPollux(self):
        root = 'SoftwareProcess/Navigation/resources/'
        sightings = root + 'pollux.xml'
        stars = root + 'stars.txt'
        arieses = root + 'aries.txt'
        arr = self.getSightings (
            sightings,
            stars,
            arieses,
            'N27d59.5',
            '85d33.4'
        )

        star = Star(stars, 'Pollux', '04/17/17')
        self.assertEqual('243d25.3', star.sha)
        self.assertEqual('27d59.1', star.declination)

        aries = Aries(arieses, '04/17/17', '23')
        self.assertEqual('191d29.9', aries.gha1)
        self.assertEqual('206d32.4', aries.gha2)

        self.assertEqual('27d59.1', arr[0].geographicPosition.lat.getString())
        self.assertEqual('87d30.8', arr[0].geographicPosition.lon.getString())

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.5\t" \
            + "84d33.4\tN27d59.5\t85d33.4\t7d21.1\t-2919",
            str(arr[0])
        )
