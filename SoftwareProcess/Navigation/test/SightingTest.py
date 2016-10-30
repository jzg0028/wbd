import unittest

import Navigation.prod.util.Sighting as Sighting

class SightingTest(unittest.TestCase):

    def testToString(self):
        root = "SoftwareProcess/Navigation/resources/"
        sightingFile = root + "sightings.xml"
        ariesFile = root + "aries.txt"
        starFile = root + "stars.txt"
        arr = Sighting.parse(sightingFile, starFile, ariesFile)

        self.assertEqual (
            "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.1\t83d43.8",
            str(arr[0])
        )
        self.assertEqual (
            "Sirius\t2017-04-17\t09:30:30\t45d11.9\t-16d44.5\t247d6.2",
            str(arr[1])
        )
