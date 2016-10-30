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
            "^LOG:\t\d{4}-\d\d-\d\d (?:\d\d:?){3}[-+]\d\d:\d\d:\t(.*)\n$"
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

        lines = self.files[-1].readlines()
        match = self.regex.match(lines[-1])
        expected = re.compile("^Log file:\t(/[^/]+)+/log\.txt$")

        self.assertEqual(1, len(lines))
        self.assertTrue(match, "bad timestamp: " + lines[-1])
        self.assertTrue(expected.match(match.group(1)))

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

        lines = self.files[-1].readlines()
        match = self.regex.match(lines[-1])
        expected = re.compile("^Log file:\t(/[^/]+)+/log\.txt$")

        self.assertEqual(1, len(lines))
        self.assertTrue(match, "bad timestamp: " + lines[-1])
        self.assertTrue(expected.match(match.group(1)))

    def testSetSightingFileValid(self):
        fix = Fix()
    # this should be valid
        fname = "SoftwareProcess/Navigation/resources/sightings.xml"

        fix.setSightingFile(self.fname)
        self.resources.append(open(self.fname, "r"))

        self.files.append(open("log.txt", "r"))

        lines = self.files[-1].readlines()
        match = self.regex.match(lines[-1])
        expected = re.compile (
            "^Sighting file:\t(/[^/]+)+/" + self.fname + "$"
        )

        self.assertEqual(2, len(lines))
        self.assertTrue(match, "bad timestamp: " + lines[-1])
        self.assertTrue(expected.match(match.group(1)))

    def testGetSightingsUnset(self):
        fix = Fix()
        self.files.append(open("log.txt", "r"))
    # undefined behavior if sighting file hasn't been set yet
        with self.assertRaises(Exception):
            fix.getSightings()

    def testGetSightingsSet(self):
        fix = Fix()
        fix.setSightingFile(self.fname)
        
        self.assertEqual(("0d0.0", "0d0.0"), fix.getSightings())

        self.files.append(open("log.txt", "r"))

        lines = self.files[-1].readlines()
        match = self.regex.match(lines[-1])
        expected = re.compile (
            "^End of sighting file (/[^/]+)+/" + self.fname + "$"
        )

        self.assertEqual(5, len(lines))
        self.assertTrue(match, "bad timestamp: " + lines[-1])
        self.assertTrue(expected.match(match.group(1)))

    def testSetAriesFileInvalid(self):
        fix = Fix()
        self.files.append(open("log.txt", "r"))

    # these are invalid names
        with self.assertRaises(ValueError):
            fix.setAriesFile("file.not-a-txt")
        with self.assertRaises(ValueError):
            fix.setAriesFile(".txt")
        with self.assertRaises(ValueError):
            fix.setAriesFile("fake.txt")

    def testSetStarFileInvalid(self):
        fix = Fix()
        self.files.append(open("log.txt", "r"))

    # these are invalid names
        with self.assertRaises(ValueError):
            fix.setStarFile("file.not-a-txt")
        with self.assertRaises(ValueError):
            fix.setStarFile(".txt")
        with self.assertRaises(ValueError):
            fix.setStarFile("fake.txt")
