import unittest

import Navigation.prod.util.Sighting as Sighting

class SightingTest(unittest.TestCase):

    def testToString(self):
        fname = "SoftwareProcess/Navigation/resources/sightings.xml"
        arr = Sighting.parse(fname)

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d01.5\t27d59.1\t84d33.4",
            str(arr[0])
        )
        self.assertEqual (
            "Sirius\t2017-04-17\t09:30:30\t45d11.9\t-16d44.5\t239d13.1",
            str(arr[1])
        )
