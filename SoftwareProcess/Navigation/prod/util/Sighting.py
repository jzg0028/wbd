import xml.etree.ElementTree as ET
import math

from Navigation.prod.Angle import Angle
from Navigation.prod.util.Star import Star
from Navigation.prod.util.Aries import Aries
import re

class GeographicPosition(object):
    def __init__(self, star, aries1, aries2, seconds):
        self.dLong = (Angle().setDegreesAndMinutes(star.hda)
        + (Angle().setDegreesAndMinutes(aries1.gha)
        + (Angle().setDegreesAndMinutes(aries2.gha)
        - Angle().setDegreesAndMinutes(aries1.gha))
        * seconds / 3600))

        self.dLat = (Angle().setDegreesAndMinutes(star.declination))

    def latitude(self):
        return Angle(self.dLat)

    def longitude(self):
        return Angle(self.dLong)

class Adjustment(object):
# CONVERT PRESSURE, TEMPERATURE TO INT
# HEIGHT TO FLOAT
    def __init__(self, observation, pressure,
        temperature, horizon, height, geographicPosition,
        assumedLatitude, assumedLongitude):

        (self.observation, self.pressure,
        self.temperature, self.horizon,
        self.height, self.geographicPosition,
        self.assumedLatitude,
        self.assumedLongitude) = (Angle().setDegreesAndMinutes(observation),
        pressure, temperature, horizon == 'Artificial',
        height, geographicPosition,
        Angle(Angle().setDegreesAndMinutes(assumedLatitude)),
        Angle(Angle().setDegreesAndMinutes(assumedLongitude)))

    def altitude(self):
        return Angle (
            self.observation
            + (0 if self.horizon else (-0.97 * math.sqrt(self.height)) / 60)
            + ((-0.00452 * self.pressure)
            / (273 + ((self.temperature - 32) * 5 / 9))
            / math.tan(math.radians(self.observation)))
        )

    def distance(self):
        rGeoLat = math.radians(self.geographicPosition.dLat)
        rAssLat = math.radians(self.assumedLatitude.getDegrees())
        rLHA = math.radians (
            self.geographicPosition.dLong - self.assumedLatitude.getDegrees()
        )

        return int(round((self.altitude().getDegrees()
                - math.asin((math.sin(rGeoLat)
                * math.sin(rAssLat))
                + (math.cos(rGeoLat)
                * math.cos(rAssLat)
                * math.cos(rLHA))))
                * 60))

    def azimuth(self):
        rGeoLat = math.radians(self.geographicPosition.dLat)
        rAssLat = math.radians(self.assumedLatitude.getDegrees())
        rDisAdj = math.radians(self.distance() / 60.0)

        return Angle (
            math.acos (
                (math.sin(rGeoLat)
                - math.sin(rAssLat)
                * math.sin(rDisAdj))
                / (math.cos(rAssLat)
                * math.cos(rDisAdj))
            )
        )

class Sighting(object):
    def __init__(self, node, starFile,
        ariesFile, assumedLatitude, assumedLongitude):

        arr = dict((child.tag, child.text) for child in node)

        (self.assLat, self.assLon, self.date,
        self.time, self.body) = (assumedLatitude,
        assumedLongitude, arr['date'],
        arr['time'], arr['body'])

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
        # negative angle is S, else positive
            self.assLat.replace('S', '-').replace('N', ''),
            self.assLon
        )

    def __str__(self):
        return (self.body
            + "\t" + self.date
            + "\t" + self.time
            + "\t" + self.adjustment.altitude().getString()
            + "\t" + self.geographicPosition.latitude().getString()
            + "\t" + self.geographicPosition.longitude().getString()
            + "\t" + self.assLat + "\t" + self.assLon
            + "\t" + self.adjustment.azimuth().getString()
            + "\t" + str(self.adjustment.distance()))
