import unittest
import os
import re

from Navigation.prod.Fix import Fix

# Note: ISO 8601 UTC date/time
class FixTest(unittest.TestCase):

    def setUp(self):
        self.fname = "SoftwareProcess/Navigation/resources/sightings.xml"
        self.files = []
        self.resources = []
        self.regex = re.compile (
            "LOG:\t\d{4}(-\d{2}){2} (\d{2}:?){3}-|\+(\d{2}:?){2}:\t"
        )

    def tearDown(self):
        for f in self.files:
            f.close()
            os.remove(f.name)
        for f in self.resources:
            f.close()

    def testConstructorInvalid(self):
    # these are invalid names
        with self.assertRaises(ValueError):
            Fix("file.not-a-txt")
        with self.assertRaises(ValueError):
            Fix(".txt")

    # these files should not have been created
        with self.assertRaises(IOError):
            self.files.append(open("file.not-a-txt", "r"))
        with self.assertRaises(IOError):
            self.files.append(open(".txt", "r"))

    def testConstructorValid(self):
    # default file name
        try:
            Fix()
            self.files.append(open("log.txt", "r"))
        except (IOError, ValueError) as e:
            self.fail(e)

    # valid file name
        try:
            Fix("foo.txt")
            self.files.append(open("foo.txt", "r"))
        except (IOError, ValueError) as e:
            self.fail(e)

    def testConstructorState(self):
        Fix()
        self.files.append(open("log.txt", "r"))

        actual = self.files[-1].readline()

    # The timestamp is unknown, but the line should always end with this.
        expected = "Start of log\n"
        self.assertEqual(expected, actual[-len(expected):])

    # The line should start with a timestamp like this regex
        self.assertTrue(self.regex.match(actual), "bad timestamp: " + actual)

# append "Start of sighting file: f.xml" to log
    def testSetSightingFileInvalid(self):
        fix = Fix()

    # these aren't valid
        with self.assertRaises(ValueError):
            fix.setSightingFile("file.not-an-xml")
        with self.assertRaises(ValueError):
            fix.setSightingFile(".xml")
        with self.assertRaises(ValueError):
            fix.setSightingFile("fake.xml")

    # log file should still only have "Start of log" in it
        self.files.append(open("log.txt", "r"))
        expected = "Start of log\n"
        actual = self.files[-1].readlines()[-1]
        self.assertEqual(expected, actual[-len(expected):])

    def testSetSightingFileValid(self):
        fix = Fix()
    # this should be valid
        fname = "SoftwareProcess/Navigation/resources/sightings.xml"

        fix.setSightingFile(self.fname)
        self.resources.append(open(self.fname, "r"))

        self.files.append(open("log.txt", "r"))
        expected = "Start of sighting file: " + self.fname + "\n"
        actual = self.files[-1].readlines()[-1]
        self.assertEqual(expected, actual[-len(expected):])

    def testGetSightingsUnset(self):
        fix = Fix()
        self.files.append(open("log.txt", "r"))
    # undefined behavior if sighting file hasn't been set yet
        with self.assertRaises(Exception):
            fix.getSightings()

    def testGetSightingsSet(self):
        fix = Fix()
        fix.setSightingFile(self.fname)
        self.files.append(open("log.txt", "r"))
        
        self.assertEqual(("0d0.0", "0d0.0"), fix.getSightings())

    # should end with this line
        expected = "End of sighting file: " + self.fname + "\n"
        lines = self.files[-1].readlines()
        actual = lines[-1]
        self.assertEqual(expected, actual[-len(expected):])
    # should be 5 lines in the log
        self.assertEqual(5, len(lines))
