"""
    October 5th 2016
    October 6th 2016
    November 20th 2016

    author: Jesse Gamez
"""

import xml.etree.ElementTree as ET

import Navigation.prod.util.Logger as Logger
from Navigation.prod.util.Sighting import Sighting
from os import path
from Navigation.prod.util.Coordinate import Coordinate
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
        try:
            with open(sightingFile, "r") as sitngs, open(self.log, "a") as log:
                log.write (
                    Logger.logify("Sighting file:\t" + sightingFile)
                )

                self.sightings = sightingFile
        except(IOError):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setSightingFile.__name__
                + ": invalid filename"
            )

    def getSightings(self, assumedLatitude = "0d0.0",
        assumedLongitude = "0d0.0"):

        if not hasattr(self, 'sightings'):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.getSightings.__name__
                + ": sighting file not set"
            )

        try:
            assumedCoordinates = Coordinate(assumedLongitude, assumedLatitude)
        except ValueError e:
            raise ValueError (
                self.__class__.name__ + '.'
                + self.getSightings.__name__
                + ': ' + e
            )

        arr = []
        with open(self.log, "a") as log:
            errors = 0
            for sighting in ET.parse(self.sightings).getroot():
                try:
                    arr.append(Sighting(sighting, self.star,
                    self.aries, assumedCoordinates))
                    log.write (
                        Logger.logify (
                            str(arr[-1])
                        )
                    )
                except:
                    errors += 1

            log.write (
                Logger.logify (
                    "Sighting errors:\t" + str(errors)
                )
            )

        Angle().setDegreesAndMinutes(assumedLatitude.replace('S', '-'))
            + sum([(i.adjustment.distance()
            * math.cos(i.adjustment.azimuth().getDegrees()))
            for i in arr]) / 60.0

        return ("0d0.0", "0d0.0")

    def setAriesFile(self, ariesFile):
        ariesFile = path.abspath(path.normpath(ariesFile))
        if re.compile("^(/[^/]+)+\.txt$").match(ariesFile) == None:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setAriesFile.__name__
                + ": invalid file name"
            )

        try:
            with open(ariesFile, "r") as aries, open(self.log, "a") as log:
                log.write (
                    Logger.logify("Aries file:\t" + ariesFile)
                )
                self.aries = ariesFile
        except(IOError):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setAriesFile.__name__
                + ": invalid file name"
            )

    def setStarFile(self, starFile):
        starFile = path.abspath(path.normpath(starFile))
        if re.compile("^(/[^/]+)+\.txt$").match(starFile) == None:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setStarFile.__name__
                + ": invalid file name"
            )

        try:
            with open(starFile, "r") as aries, open(self.log, "a") as log:
                log.write (
                    Logger.logify("Star file:\t" + starFile)
                )
                self.star = starFile
        except(IOError):
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setStarFile.__name__
                + ": invalid file name"
            )
