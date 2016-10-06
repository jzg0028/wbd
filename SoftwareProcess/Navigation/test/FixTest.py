import unittest
from Navigation.prod.Fix import Fix

# Note: ISO 8601 UTC date/time
class FixTest(unittest.TestCase):

    def constructorTest(self):
    # these are invalid names
        with self.assertRaises(ValueError):
            Fix("file.not-a-txt")
        with self.assertRaises(ValueError):
            Fix(".txt")

    # these files should not have been created
        with self.assertRaises(FileNotFoundError):
            open("file.not-a-txt", "r")
        with self.assertRaises(FileNotFoundError):
            open(".txt", "r")

    # default file name
        try:
            Fix()
            open("log.txt", "r")
        except (FileNotFoundError, ValueError) as e:
            self.fail(e)

    # valid file name
        try:
            Fix("foo.txt")
            open("foo.txt", "r")
        except (FileNotFoundError, ValueError) as e:
            self.fail(e)

# instructions are unclear
# append "Start of sighting file: f.xml" to log
    def setSightingFileTest(self):
    # these are invalid names
        with self.assertRaises(ValueError):
            Fix("file.not-an-xml")
        with self.assertRaises(ValueError):
            Fix(".xml")

    # these files should not have been created
        with self.assertRaises(FileNotFoundError):
            open("file.not-an-xml", "r")
        with self.assertRaises(FileNotFoundError):
            open(".xml", "r")

# append sightings from XML file to log
# apped "End of sighting file: f.xml" to log
    def getSightingsTest(self):
        pass
