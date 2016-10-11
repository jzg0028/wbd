import xml.etree.ElementTree as ET
import math

from Navigation.prod.Angle import Angle

def parse(fname):
    return tuple((Sighting(sighting))
        for sighting in ET.parse(fname).getroot())

class Sighting(object):
    def __init__(self, node):
        self.arr = dict((child.tag, child.text) for child in node)

    def adjustedAltitude(self):
        altitude = Angle().setDegreesAndMinutes(self.arr["observation"])

        refraction = ((-0.00452 * int(self.arr["pressure"]))
            / (273 + ((int(self.arr["temperature"]) - 32) * 5 / 9))
            / math.tan(math.radians(altitude)))

        dip = (0 if self.arr["horizon"] == "Artificial"
        else (-0.97 * math.sqrt(float(self.arr["height"]))) / 60)

        return altitude + dip + refraction
    def __str__(self):
        return (self.arr["body"]
            + "\t" + self.arr["date"]
            + "\t" + self.arr["time"]
            + "\t" + Angle(self.adjustedAltitude()).getString())
