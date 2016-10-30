import xml.etree.ElementTree as ET
import math

from Navigation.prod.Angle import Angle
from Navigation.prod.util.Star import Star
from Navigation.prod.util.Aries import Aries
import re

def parse(sightingFile, starFile, ariesFile):
    return tuple((Sighting(sighting, starFile, ariesFile))
        for sighting in ET.parse(sightingFile).getroot())

class Sighting(object):
    def __init__(self, node, starFile, ariesFile):
        self.arr = dict((child.tag, child.text) for child in node)

        date = self.date()
        hour = self.hour()
        self.star = Star(starFile, self.arr["body"], date)
        self.aries = Aries(ariesFile, date, hour)

    def adjustedAltitude(self):
        altitude = Angle().setDegreesAndMinutes(self.arr["observation"])

        refraction = ((-0.00452 * int(self.arr["pressure"]))
            / (273 + ((int(self.arr["temperature"]) - 32) * 5 / 9))
            / math.tan(math.radians(altitude)))

        dip = (0 if self.arr["horizon"] == "Artificial"
        else (-0.97 * math.sqrt(float(self.arr["height"]))) / 60)

        return altitude + dip + refraction

    def geographicLatitude(self):
        return self.star.declination

    def date(self):
        match = re.compile("^\d\d(\d\d)-(\d\d)-(\d\d)$").match(self.arr["date"])

        return match.group(2) + "/" + match.group(3) + "/" + match.group(1)

    def hour(self):
        match = re.compile("^0?([1-9]?\d):\d\d:\d\d$").match(self.arr["time"])

        return match.group(1)

    def geographicLongitude(self):
        sha, gha = (Angle(),)*2
        sha.setDegreesAndMinutes(self.star.sha)
        gha.setDegreesAndMinutes(self.aries.gha)

        return sha.add(gha)

    def __str__(self):
        return (self.arr["body"]
            + "\t" + self.arr["date"]
            + "\t" + self.arr["time"]
            + "\t" + Angle(self.adjustedAltitude()).getString()
            + "\t" + Angle(self.geographicLatitude()).getString()
            + "\t" + Angle(self.geographicLongitude()).getString())
