"""
    October 6th 2016

    author: Jesse Gamez
"""

from datetime import datetime

def logify(string):
    return ("LOG: " +
        datetime.utcnow().isoformat(' ') +
        ": " +
        string +
        "\n")
