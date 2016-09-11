"""
    September 10th 2016

    author: Jesse Gamez
"""

import unittest

from Angle import Angle

class AngleTest(unittest.TestCase):
    def test_setDegrees(self):
        angle = Angle()

    # 360
        self.assertEqual(angle.setDegrees(360), 0)

    # 0 = 360
        self.assertEqual(angle.setDegrees(0), 0)

    # between 0 and 360
        self.assertEqual(angle.setDegrees(180), 180)

    # over 360
        self.assertEqual(angle.setDegrees(361), 1)

    # 361 = 1 if 360 = 0
        self.assertEqual(angle.setDegrees(1), 1)

    # under 0
        self.assertEqual(angle.setDegrees(-1), 359)

    # -361 = -1 if -360 = 0
        self.assertEqual(angle.setDegrees(-361), 359)

    # 720 = 360 = 0
        self.assertEqual(angle.setDegrees(720), 0)

    # -720 = -360 = 0
        self.assertEqual(angle.setDegrees(-720), 0)

    # 721 = 361 = 1
        self.assertEqual(angle.setDegrees(721), 1)

    # -721 = -361 = -1
        self.assertEqual(angle.setDegrees(-721), 359)

    # persistance test
        self.assertEqual(angle.getDegrees(), 359)

    # default value
        self.assertEqual(angle.setDegrees(), 0)

        with self.assertRaises(ValueError):
            angle.setDegrees("abc")

    def test_getDegrees(self):
        angle = Angle()

        angle.setDegrees(90)
        self.assertEqual(angle.getDegrees(), 90)

    def test_setDegreesAndMinutes(self):
        angle = Angle()

    # valid inputs
        try:
        # 60 minutes = 1 degrees
            self.assertEqual(angle.setDegreesAndMinutes("0d60.0"), 1)
        
        # 0 minutes
            self.assertEqual(angle.setDegreesAndMinutes("0d0.0"), 0)

        # 30 minutes = 0.5 degrees
            self.assertEqual(angle.setDegreesAndMinutes("0d30.0"), 0.5)

        # 120 minutes = 2 degrees
            self.assertEqual(angle.setDegreesAndMinutes("0d120.0"), 2)

        # 1 degrees 120 minutes = 3 degrees
            self.assertEqual(angle.setDegreesAndMinutes("1d120.0"), 3)

        # 360 degrees 60 minutes = 1 degrees if 360 degrees = 0 degrees
            self.assertEqual(angle.setDegreesAndMinutes("360d60.0"), 1)

        # -1 degrees 60 minutes = 0 degrees
            self.assertEqual(angle.setDegreesAndMinutes("-1d60.0"), 0)

        except Exception:
        # none of these valid inputs should throw an exception
            self.assertTrue(False)

    # string must not be empty
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("")

    # no negative minutes
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("0d-1.0")

    # missing degrees
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("d1.0")

    # missing minutes
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("0d")

    # missing separator
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("5")

    # degrees must be integer
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("0.1d0")

    # minutes must have no more than one decimal place
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("5d0.11")

    # minutes must have no less than one decimal place
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("5d1")

    # must be numbers
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("xd5")
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("4dy")

    # separator must be a 'd'
        with self.assertRaises(ValueError):
            angle.setDegreesAndMinutes("5:3")

    # persistance tests
        angle.setDegreesAndMinutes("180d60.0")
        self.assertEqual(angle.getDegrees(), 181)
        try:
            angle.setDegreesAndMinutes("")
        except:
            pass
        self.assertEqual(angle.getDegrees(), 181)

    def test_getString(self):
        angle = Angle()

        angle.setDegrees(60.5)
        self.assertEqual(angle.getString(), "60d30.0")

        angle.setDegrees(45.123)
        self.assertEqual(angle.getString(), "45d7.4")

    def test_getStringSetDegreesAndMinutesCommutative(self):
        a = Angle()
        b = Angle()

        a.setDegreesAndMinutes("180d40.8")
        b.setDegreesAndMinutes(a.getString())

        self.assertEqual(b.getString(), "180d40.8")

    def test_add(self):
        a = Angle()
        b = Angle()

    # typical
        a.setDegrees(1)
        b.setDegrees(1)
        self.assertEqual(a.add(b), 2)

    # float
        a.setDegrees(0)
        b.setDegrees(0.5)
        self.assertEqual(a.add(b), 0.5)

    # overflow
        a.setDegrees(360)
        b.setDegrees(1)
        self.assertEqual(a.add(b), 1)

    # double overflow
        a.setDegrees(360)
        b.setDegrees(361)
        self.assertEqual(a.add(b), 1)

    # persistance test
        a.setDegrees(1)
        b.setDegrees(1)
        a.add(b)
        self.assertEqual(a.getDegrees(), 2)

    def test_subtract(self):
        a = Angle()
        b = Angle()

    # typical
        a.setDegrees(360)
        b.setDegrees(1)
        self.assertEqual(a.subtract(b), 359)

    # overflow
        a.setDegrees(0)
        b.setDegrees(1)
        self.assertEqual(a.subtract(b), 359)

    # double overflow
        a.setDegrees(0)
        b.setDegrees(361)
        self.assertEqual(a.subtract(b), 359)

    # persistance test
        a.setDegrees(2)
        b.setDegrees(1)
        a.subtract(b)
        self.assertEqual(a.getDegrees(), 1)

    def test_compare(self):
        a = Angle()
        b = Angle()

    # typical less
        a.setDegrees(0)
        b.setDegrees(1)
        self.assertTrue(a.compare(b) == -1)

    # typical greater
        a.setDegrees(1)
        b.setDegrees(0)
        self.assertTrue(a.compare(b) == 1)

    # typical equal
        a.setDegrees(1)
        b.setDegrees(1)
        self.assertTrue(a.compare(b) == 0)

    # 360 = 0
        a.setDegrees(360)
        b.setDegrees(0)
        self.assertTrue(a.compare(b) == 0)

    # 180 > 360
        a.setDegrees(180)
        b.setDegrees(360)
        self.assertTrue(a.compare(b) == 1)

    # 180 < -1
        a.setDegrees(180)
        b.setDegrees(-1)
        self.assertTrue(a.compare(b) == -1)

    # no state change
        self.assertEqual(a.getDegrees(), 180)
