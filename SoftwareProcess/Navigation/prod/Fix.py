"""
    October 5th 2016
    October 6th 2016

    author: Jesse Gamez
"""

import Navigation.prod.util.Logger as Logger

class Fix(object):

    def __init__(self, name = "log.txt"):
        if name.count(".txt") == 0 or name[-5:] == ".txt":
            raise ValueError

    # must store name instead of FD to avoid zombie FD
        self.log = name
        f = open(name, "a")
        f.write(Logger.logify("Start of log"))
        f.close()

    def setSightingFile(self, name):
        if name.count(".xml") == 0 or name[-5:] == ".xml":
            raise ValueError
        self.sightings = name

        sightings = open(name, "a")
        log = open(self.log, "a")
        log.write(Logger.logify("Start of sighting file: " + name))
        log.close()
        sightings.close()

    def getSightings():
        pass
