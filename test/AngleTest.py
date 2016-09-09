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

    def test_getDegrees(self):
        angle = Angle()

        angle.setDegrees(90)
        self.assertEqual(angle.getDegrees(), 90)

    def test_setDegreesAndMinutes(self):
        angle = Angle()

    # valid inputs
        try:
        # 60 minutes = 1 degrees
            self.assertEqual(angle.setDegreesAndMinutes("0d60"), 1)
        
        # 0 minutes
            self.assertEqual(angle.setDegreesAndMinutes("0d0"), 0)

        # 30 minutes = 0.5 degrees
            self.assertEqual(angle.setDegreesAndMinutes("0d30"), 0.5)

        # 120 minutes = 2 degrees
            self.assertEqual(angle.setDegreesAndMinutes("0d120"), 2)

        # 1 degrees 120 minutes = 3 degrees
            self.assertEqual(angle.setDegreesAndMinutes("1d120"), 3)

        # 360 degrees 60 minutes = 1 degrees if 360 degrees = 0 degrees
            self.assertEqual(angle.setDegreesAndMinutes("360d60"), 1)

        # -1 degrees 60 minutes = 0 degrees
            self.assertEqual(angle.setDegreesAndMinutes("-1d660"), 0)

        except Exception:
        # none of these valid inputs should throw an exception
            self.assertFail()

    # string must not be empty
        self.assertRaises(ValueError, angle.setDegreesAndMinutes(""))

    # no negative minutes
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("0d-1"))

    # missing degrees
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("d1"))

    # missing minutes
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("0d"))

    # missing separator
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("5"))

    # degrees must be integer
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("0.1d0"))

    # minutes must have one decimal place
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("5d0.11"))

    # must be numbers
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("xd5"))
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("4dy"))
        
    # separator must be a 'd'
        self.assertRaises(ValueError, angle.setDegreesAndMinutes("5:3"))

    # persistance tests
        angle.setDegreesAndMinutes("180d60")
        self.assertEqual(angle.getDegrees(), 181)
        angle.setDegreesAndMinutes("")
        self.assertEqual(angle.getDegrees(), 181)

    def test_getString(self):
        angle = Angle()

        angle.setDegrees(60.5)
        self.assertEqual("60d30", angle.getString())

        angle.setDegrees(45.123)
        self.assertEqual("45d7.4", angle.getString())

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
