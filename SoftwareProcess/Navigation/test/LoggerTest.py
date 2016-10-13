import unittest
import re

import Navigation.prod.util.Logger as Logger

class LoggerTest(unittest.TestCase):

    def testLogify(self):
        msg = "foobar"
        actual = Logger.logify(msg)
        match = re.compile(
            "^LOG:\t\d{4}-\d\d-\d\d (?:\d\d:?){3}[-+]\d\d:\d\d:\t(.*)\n$"
        ).match(actual)
        
        self.assertTrue(match, "bad timestamp: " + actual)

        self.assertEqual(msg, match.group(1))
