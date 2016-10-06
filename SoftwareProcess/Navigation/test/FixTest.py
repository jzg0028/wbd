import unittest
import os
from Navigation.prod.Fix import Fix

# Note: ISO 8601 UTC date/time
class FixTest(unittest.TestCase):

    def setUp(self):
        self.files = []

    def tearDown(self):
        for f in self.files:
            f.close()
            os.remove(f.name)

    def testConstructor(self):
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

# instructions are unclear
# append "Start of sighting file: f.xml" to log
    def testSetSightingFile(self):
    # these are invalid names
        with self.assertRaises(ValueError):
            Fix("file.not-an-xml")
        with self.assertRaises(ValueError):
            Fix(".xml")

    # these files should not have been created
        with self.assertRaises(FileNotFoundError):
            self.files.append(open("file.not-an-xml", "r"))
        with self.assertRaises(FileNotFoundError):
            self.files.append(open(".xml", "r"))

    def testGetSightings(self):
        pass
