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

        self.assertEqual('243d25.3',
            arr[0].geographicPosition.star.sha)
        self.assertEqual('27d59.1',
            arr[0].geographicPosition.star.declination)

        self.assertEqual('04/17/17',
            arr[0].geographicPosition.aries.date)
        self.assertEqual('27d59.1',
            arr[0].geographicPosition.latitude().getString())
        self.assertEqual('87d30.8',
            arr[0].geographicPosition.longitude().getString())

        self.assertEqual('173d4.2',
            arr[0].adjustment.lha().getString())

        self.assertAlmostEqual(-0.5538,
            arr[0].adjustment.intermediateDistance(), 4)

        self.assertAlmostEqual(-33.6304,
            arr[0].adjustment.correctedAltitude(), 4)

        self.assertEqual('15d1.5',
            arr[0].adjustment.altitude().getString())

        self.assertEqual(-2919, arr[0].adjustment.distance())

        self.assertAlmostEqual(0.729178,
            arr[0].adjustment.azimuthNumerator(), 4)
        self.assertAlmostEqual(0.735223,
            arr[0].adjustment.azimuthDenominator(), 4)

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.5\t" \
            + "84d33.4\tN27d59.5\t85d33.4\t7d21.1\t-2919",
            str(arr[0])
        )
