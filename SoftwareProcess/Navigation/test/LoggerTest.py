import unittest
import re

import Navigation.prod.util.Logger as Logger

class LoggerTest(unittest.TestCase):

    def testLogifyTimestamp(self):
        regex = re.compile(
            "LOG:\t\d{4}(-\d{2}){2} (\d{2}:?){3}-(\d{2}:?){2}:\t"
        )
        actual = Logger.logify("foobar")
        self.assertTrue(regex.match(actual), "bad timestamp: " + actual)

    def testLogifyNewline(self):
        self.assertEqual("\n", Logger.logify("foobar")[-1])

    def testLogifyMessage(self):
        foo = "foobar"
        self.assertEqual(foo, Logger.logify(foo)[-len(foo) - 1 : -1])
