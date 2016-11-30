import unittest

from Navigation.prod.util.Coordinate import Coordinate
from Navigation.prod.Angle import Angle
import re

class CoordinateTest(unittest.TestCase):
    def testByAngle(self):
        exp = re.compile (
            '^(0?0?0d0?0\.0|' \
            + '[NS]0?(([1-8]\d|' \
            + '0?[1-9])d(\d?\d\.\d)|'
            + '0?0?0d([1-5]\d\.\d|'
            + '0?[1-9]\.\d|'
            + '0?0\.[1-9])))$'
        )

        for i in xrange(-720, 720):
            latStr = Coordinate(Angle(i), Angle(0.0)).latStr()
            self.assertTrue (
                exp.match(latStr),
                'bad latitude: str: ' + latStr + ' num: ' + str(i)
            )

    def testByDegree(self):
        exp = re.compile (
            '^(0?0?0d0?0\.0|' \
            + '[NS]0?(([1-8]\d|' \
            + '0?[1-9])d(\d?\d\.\d)|'
            + '0?0?0d([1-5]\d\.\d|'
            + '0?[1-9]\.\d|'
            + '0?0\.[1-9])))$'
        )

        for i in xrange(-720, 720):
            latStr = Coordinate(i, 0.0).latStr()
            self.assertTrue (
                exp.match(latStr),
                'bad latitude: str: ' + latStr + ' num: ' + str(i)
            )

    def testByStr(self):
        self.assertEqual (
            'N1d0.0',
            Coordinate(Angle(181), Angle(0.0)).latStr()
        )
        self.assertEqual (
            'N1d0.0',
            Coordinate(Angle(91), Angle(0.0)).latStr()
        )
        self.assertEqual (
            'S1d0.0',
            Coordinate(Angle(-181), Angle(0.0)).latStr()
        )
        self.assertEqual (
            'S1d0.0',
            Coordinate(Angle(-91), Angle(0.0)).latStr()
        )
        self.assertEqual (
            'S89d0.0',
            Coordinate(Angle(-359), Angle(0.0)).latStr()
        )

        self.assertEqual (
            'S1d0.0',
            Coordinate('S1d0.0', '0d0.0').latStr()
        )
        self.assertEqual (
            'N1d0.0',
            Coordinate('N1d0.0', '0d0.0').latStr()
        )
        self.assertEqual (
            'S89d0.0',
            Coordinate('S89d0.0', '0d0.0').latStr()
        )
