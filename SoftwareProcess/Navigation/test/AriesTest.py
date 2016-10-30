import unittest
from Navigation.prod.util.Aries import Aries

class AriesTest(unittest.TestCase):

    def testValidDate(self):
        fname = "SoftwareProcess/Navigation/resources/aries.txt"
        aries = Aries(fname, "01/11/17", "13")

        self.assertEqual(aries.gha, "305d28.9")

    def testInvalidDate(self):
        fname = "SoftwareProcess/Navigation/resources/aries.txt"
        
        with self.assertRaises(ValueError):
            Aries(fname, "01/11/18", "13")
