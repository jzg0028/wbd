import unittest
from Navigation.prod.util.Star import Star

class StarTest(unittest.TestCase):

    def testEqualDate(self):
        fname = "SoftwareProcess/Navigation/resources/stars.txt"
        star = Star(fname, "Menkar", "01/04/17")

        self.assertEqual(star.hda, "314d13.0")
        self.assertEqual(star.declination, "4d09.0")

    def testGreaterDate(self):
        fname = "SoftwareProcess/Navigation/resources/stars.txt"
        star = Star(fname, "Menkar", "01/05/17")

        self.assertEqual(star.hda, "314d13.0")
        self.assertEqual(star.declination, "4d09.0")
