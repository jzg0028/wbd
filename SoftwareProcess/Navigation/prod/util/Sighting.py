import xml.etree.ElementTree as ET
import math

from Navigation.prod.Angle import Angle
from Navigation.prod.util.Star import Star
from Navigation.prod.util.Aries import Aries
import re

class Sighting(object):
    def __init__(self, node, starFile,
        ariesFile, assumedLatitude, assumedLongitude):

        self.arr = dict((child.tag, child.text) for child in node)

        self.assLat, self.assLon = assumedLatitude, assumedLongitude

        date = self.date()
        hour = self.hour()
        self.star = Star(starFile, self.arr["body"], date)
        self.aries1 = Aries(ariesFile, date, str(hour))
        self.aries2 = Aries(ariesFile, date, str((hour + 1) % 24))

    def adjustedAltitude(self):
        altitude = Angle().setDegreesAndMinutes(self.arr["observation"])

        refraction = ((-0.00452 * int(self.arr["pressure"]))
            / (273 + ((int(self.arr["temperature"]) - 32) * 5 / 9))
            / math.tan(math.radians(altitude)))

        dip = (0 if self.arr["horizon"] == "Artificial"
        else (-0.97 * math.sqrt(float(self.arr["height"]))) / 60)

        return Angle(altitude + dip + refraction)

    def geographicLatitude(self):
        a = Angle()
        a.setDegreesAndMinutes(self.star.declination)
        return a

    def date(self):
        match = re.compile("^\d\d(\d\d)-(\d\d)-(\d\d)$").match(self.arr["date"])

        return match.group(2) + "/" + match.group(3) + "/" + match.group(1)

    def hour(self):
        match = re.compile("^(\d\d):\d\d:\d\d$").match(self.arr["time"])

        return int(match.group(1))

    def seconds(self):
        match = re.compile("^\d\d:(\d\d):(\d\d)").match(self.arr["time"])
        
        return (int(match.group(1)) * 60) + int(match.group(2))

    def geographicLongitude(self):
        hda = Angle()
        hda.setDegreesAndMinutes(self.star.hda)
        hda.add(self.ghaAries())
        return hda

    def ghaAries(self):
        gha1 = Angle()
        gha1.setDegreesAndMinutes(self.aries1.gha)

        gha1.add(Angle(self.subAries().getDegrees() * self.seconds() / 3600))

        return gha1

    def subAries(self):
        gha1 = Angle()
        gha2 = Angle()
        gha1.setDegreesAndMinutes(self.aries1.gha)
        gha2.setDegreesAndMinutes(self.aries2.gha)

        gha2.subtract(gha1)

        return gha2

    def localHourAngle(self):
        return Angle (
            self.geographicLongitude().getDegrees()
            - Angle().setDegreesAndMinutes(self.assLon)
        )

    def correctedAltitude(self):
        rGeoLat = math.radians(self.geographicLatitude().getDegrees())
        rAssLat = math.radians(Angle().setDegreesAndMinutes(self.assLat[1:]))
        rLHA = math.radians(self.localHourAngle().getDegrees())

        return Angle (
            math.asin (
                (math.sin(rGeoLat)
                * math.sin(rAssLat))
                + (math.cos(rGeoLat)
                * math.cos(rAssLat)
                * math.cos(rLHA))
            )
        )

    def distanceAdjustment(self):
        return int (
            round (
                (self.adjustedAltitude().getDegrees()
                - self.correctedAltitude().getDegrees())
                * 60
            )
        )

    def azimuthAdjustment(self):
        rGeoLat = math.radians(self.geographicLatitude().getDegrees())
        rAssLat = math.radians(Angle().setDegreesAndMinutes(self.assLat[1:]))
        rDisAdj = math.radians (self.distanceAdjustment() / 60.0)

        return Angle (
            math.acos (
                (math.sin(rGeoLat)
                - math.sin(rAssLat)
                * math.sin(rDisAdj))
                / (math.cos(rAssLat)
                * math.cos(rDisAdj))
            )
        )

    def __str__(self):
        return (self.arr["body"]
            + "\t" + self.arr["date"]
            + "\t" + self.arr["time"]
            + "\t" + self.adjustedAltitude().getString()
            + "\t" + self.geographicLatitude().getString()
            + "\t" + self.geographicLongitude().getString()
            + "\t" + self.assLat + "\t" + self.assLon
            + "\t" + self.azimuthAdjustment().getString()
            + "\t" + str(self.distanceAdjustment()))
