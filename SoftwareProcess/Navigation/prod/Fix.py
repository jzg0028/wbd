"""
    October 5th 2016
    October 6th 2016

    author: Jesse Gamez
"""

import xml.etree.ElementTree as ET

import Navigation.prod.util.Logger as Logger
import Navigation.prod.util.Sighting as Sighting
from os import path
import re


class Fix(object):

    def __init__(self, logFile = "log.txt"):
        logFile = path.abspath(path.normpath(logFile))
        if re.compile("^(/[^/]+)+\.txt$").match(logFile) == None:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.__init__.__name__
                + ": invalid filename"
            )

    # must store logFile instead of FD to avoid zombie FD
        self.log = logFile

        try:
            with open(logFile, "a") as log:
                log.write(Logger.logify("Log file:\t" + logFile))
        except(IOError):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.__init__.__name__
                + ": invalid filename"
            )

    def setSightingFile(self, sightingFile):
        sightingFile = path.abspath(path.normpath(sightingFile))
        if re.compile("^(/[^/]+)+\.xml$").match(sightingFile) == None:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setSightingFile.__name__
                + ": invalid filename"
            )

    # store name instead of FD to avoid zombie FD
        self.sightings = sightingFile

        try:
            with open(sightingFile, "r") as sitngs, open(self.log, "a") as log:
                log.write (
                    Logger.logify("Sighting file:\t" + sightingFile)
                )
        except(IOError):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setSightingFile.__name__
                + ": invalid filename"
            )

    def getSightings(self):
        if not hasattr(self, 'sightings'):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.getSightings.__name__
                + ": sighting file not set"
            )

    # any errors at this point are undefined
        with open(self.log, "a") as log:
            for sighting in Sighting.parse(self.sightings):
                log.write(Logger.logify(str(sighting)))
            log.write (
                Logger.logify (
                    "End of sighting file " + self.sightings
                )
            )
            return ("0d0.0", "0d0.0")

    def setAriesFile(self, ariesFile):
        ariesFile = path.abspath(path.normpath(ariesFile))
        if re.compile("^(/[^/]+)+\.txt$").match(ariesFile) == None:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setAriesFile.__name__
                + ": invalid file name"
            )
