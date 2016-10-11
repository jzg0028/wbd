import unittest

import Navigation.prod.util.Sighting as Sighting

class SightingTest(unittest.TestCase):

    def testToString(self):
        fname = "SoftwareProcess/Navigation/resources/sightings.xml"
        arr = Sighting.parse(fname)

        self.assertEqual (
            "Aldebran\t2016-03-01\t23:40:01\t15d1.5",
            str(arr[0])
        )
        self.assertEqual (
            "Peacock\t2016-03-02\t00:05:05\t45d11.9",
            str(arr[1])
        )
