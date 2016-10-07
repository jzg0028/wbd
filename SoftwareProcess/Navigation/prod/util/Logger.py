"""
    October 6th 2016

    author: Jesse Gamez
"""

from datetime import datetime, tzinfo, timedelta
import time

class TimeZone(tzinfo):
    def utcoffset(self, dt):
        return -timedelta(seconds = time.timezone)

def logify(string):
    return ("LOG:\t" +
        datetime.utcnow()
            .replace(tzinfo = TimeZone(), microsecond = 0)
            .isoformat(' ') +
        ":\t" +
        string +
        "\n")
