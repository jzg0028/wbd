import unittest
import os
import re

from Navigation.prod.Fix import Fix

# Note: ISO 8601 UTC date/time
class FixTest(unittest.TestCase):

    def setUp(self):
        self.files = []
        self.regex = re.compile("LOG: \d{4}(-\d{2}){2} (\d{2}:?){3}\.\d{6}:")

    def tearDown(self):
        for f in self.files:
            f.close()
            os.remove(f.name)

    def testConstructorInvalid(self):
    # these are invalid names
        with self.assertRaises(ValueError):
            Fix("file.not-a-txt")
        with self.assertRaises(ValueError):
            Fix(".txt")

    # these files should not have been created
        with self.assertRaises(FileNotFoundError):
            self.files.append(open("file.not-a-txt", "r"))
        with self.assertRaises(FileNotFoundError):
            self.files.append(open(".txt", "r"))

    def testConstructorValid(self):
    # default file name
        try:
            Fix()
            self.files.append(open("log.txt", "r"))
        except (FileNotFoundError, ValueError) as e:
            self.fail(e)

    # valid file name
        try:
            Fix("foo.txt")
            self.files.append(open("foo.txt", "r"))
        except (FileNotFoundError, ValueError) as e:
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

# instructions are unclear
# append "Start of sighting file: f.xml" to log
    def testSetSightingFileInvalid(self):
        fix = Fix()

    # these aren't valid
        with self.assertRaises(ValueError):
            fix.setSightingFile("file.not-an-xml")
        with self.assertRaises(ValueError):
            fix.setSightingFile(".xml")

    # log file should still only have "Start of log" in it
        self.files.append(open("log.txt", "r"))
        expected = "Start of log\n"
        self.assertEqual(expected, self.files[-1].readline()[-len(expected):])

    def testGetSightings(self):
        pass
