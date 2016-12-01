import xml.etree.ElementTree as ET
import math

from Navigation.prod.Angle import Angle
from Navigation.prod.util.Star import Star
from Navigation.prod.util.Aries import Aries
from Navigation.prod.util.Coordinate import Coordinate
import re

class GeographicPosition(object):
    def __init__(self, star, aries1, aries2, seconds):
        self.lon = Angle((Angle().setDegreesAndMinutes(star.sha)
        + (Angle().setDegreesAndMinutes(aries1.gha)
        + (Angle().setDegreesAndMinutes(aries2.gha)
        - Angle().setDegreesAndMinutes(aries1.gha))
        * seconds / 3600)))

        self.lat = Angle(Angle().setDegreesAndMinutes(star.declination))

    def latitude(self):
        return self.lat

    def longitude(self):
        return self.lon

class Adjustment(object):
# CONVERT PRESSURE, TEMPERATURE TO INT
# HEIGHT TO FLOAT
    def __init__(self, observation, pressure,
        temperature, horizon, height, geographicPosition,
        assumedCoordinates):

        (self.observation, self.pressure,
        self.temperature, self.horizon,
        self.height, self.geographicPosition,
        self.assumedCoordinates) = (Angle().setDegreesAndMinutes(observation),
        pressure, temperature, horizon == 'Artificial',
        height, geographicPosition, assumedCoordinates)

    def altitude(self):
        return Angle (
            self.observation
            + (0 if self.horizon else (-0.97 * math.sqrt(self.height)) / 60)
            + ((-0.00452 * self.pressure)
            / (273 + ((self.temperature - 32) * 5 / 9))
            / math.tan(math.radians(self.observation)))
        )

    def distance(self):
        return int(round((self.altitude().getDegrees()
            - self.correctedAltitude()) * 60))

    def correctedAltitude(self):
        return math.asin(self.intermediateDistance())

    def intermediateDistance(self):
        rGeoLat = math.radians(self.geographicPosition.lat.getDegrees())
        rAssLat = math.radians (
            self.assumedCoordinates.lat
        )
        rLHA = math.radians (
            self.geographicPosition.lon.getDegrees()
            - self.assumedCoordinates.lon
        )

        return ((math.sin(rGeoLat)
            * math.sin(rAssLat))
            + (math.cos(rGeoLat)
            * math.cos(rAssLat)
            * math.cos(rLHA)))

    def azimuthNumerator(self):
        rGeoLat = math.radians(self.geographicPosition.lat.getDegrees())
        rAssLat = math.radians (
            self.assumedCoordinates.lat
        )

        return (math.sin(rGeoLat)
        - math.sin(rAssLat)
        * self.intermediateDistance())

    def intermediateAzimuth(self):
        return self.azimuthNumerator() / self.azimuthDenominator()

    def azimuthDenominator(self):
        rCorAlt = math.radians(self.correctedAltitude())
        rAssLat = math.radians (
            self.assumedCoordinates.lat
        )

        return (math.cos(rAssLat) * math.cos(rCorAlt))

    def azimuth(self):
        return Angle(math.acos(self.intermediateAzimuth()))

class Sighting(object):
    def __init__(self, node, starFile,
        ariesFile, assumedCoordinates):

        arr = dict((child.tag, child.text) for child in node)

        (self.assumedCoordinates, self.date,
        self.time, self.body) = (assumedCoordinates,
        arr['date'], arr['time'], arr['body'])

        match = re.compile('^\d\d(\d\d)-(\d\d)-(\d\d)$') \
            .match(arr['date'])
        date = match.group(2) + '/' + match.group(3) + '/' + match.group(1)

        match = re.compile('^(\d\d):(\d\d):(\d\d)$').match(arr['time'])
        hour = int(match.group(1))
        seconds = (int(match.group(2)) * 60) + int(match.group(3))

        self.geographicPosition = GeographicPosition (
            Star(starFile, arr['body'], date),
            Aries(ariesFile, date, str(hour)),
            Aries(ariesFile, date, str((hour + 1) % 24)),
            seconds
        )

        self.adjustment = Adjustment (
            arr['observation'],
            int(arr['pressure']),
            int(arr['temperature']),
            arr['horizon'],
            float(arr['height']),
            self.geographicPosition,
            self.assumedCoordinates
        )

    def __str__(self):
        return (self.body
            + "\t" + self.date
            + "\t" + self.time
            + "\t" + self.adjustment.altitude().getString()
            + "\t" + self.geographicPosition.lat.getString()
            + "\t" + self.geographicPosition.lon.getString()
            + "\t" + self.assumedCoordinates.latStr()
            + "\t" + self.assumedCoordinates.lonStr()
            + "\t" + self.adjustment.azimuth().getString()
            + "\t" + str(self.adjustment.distance()))
