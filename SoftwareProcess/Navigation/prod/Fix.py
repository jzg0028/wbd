"""
    October 5th 2016
    October 6th 2016

    author: Jesse Gamez
"""

import xml.etree.ElementTree as ET

import Navigation.prod.util.Logger as Logger
import Navigation.prod.util.Sighting as Sighting

class Fix(object):

    def __init__(self, name = "log.txt"):
        if name.count(".txt") == 0 or name[-5:] == ".txt":
            raise ValueError

    # must store name instead of FD to avoid zombie FD
        self.log = name

        try:
            with open(name, "a") as log:
                log.write(Logger.logify("Start of log"))
        except(IOError):
            raise ValueError

    def setSightingFile(self, name):
        if name.count(".xml") == 0 or name[-5:] == ".xml":
            raise ValueError

    # store name instead of FD to avoid zombie FD
        self.sightings = name

        try:
            with open(name, "r") as sightings, open(self.log, "a") as log:
                log.write(Logger.logify("Start of sighting file: " + name))
        except(IOError):
            raise ValueError

    def getSightings(self):
    # any errors at this point are undefined
        with open(self.log, "a") as log:
            for sighting in Sighting.parse(self.sightings):
                log.write(Logger.logify(str(sighting)))
            log.write (
                Logger.logify (
                    "End of sighting file: " + self.sightings
                )
            )
