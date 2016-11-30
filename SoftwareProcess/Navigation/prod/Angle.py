"""
    September 10th 2016

    author: Jesse Gamez
"""
import re

class Angle(object):
    __period = 360
    __minute = 60

    def __init__(self, degrees = 0):
        self.setDegrees(degrees)

    def setDegrees(self, degrees = 0):
        try:
            degrees = float(degrees)
        except:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.setDegrees.__name__
                + ":  doesn't look like a float"
            )

    # recursively add 360 to the degrees until its positive
        if degrees < 0:
            return self.setDegrees(degrees + self.__period)

    # set the positive degrees as % 360
        self.angle = degrees % self.__period

        return self.getDegrees()

    def setDegreesAndMinutes(self, degrees):
        match = re.compile("^(-?)(\d{1,3})d(\d{1,2}\.\d)$").match(degrees)

    # if the regex found a match in degrees
        if match:
        # return degrees + minutes / minute
            return self.setDegrees (
                int(match.group(1) + match.group(2))
                + float(match.group(1) + match.group(3))
                / self.__minute
            )

    # otherwise, raise an error
        raise ValueError (
            self.__class__.__name__ + "."
            + self.setDegreesAndMinutes.__name__
            + ":  invalid string format: " + degrees
        )

    def add(self, angle):
        if type(angle) is not Angle:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.add.__name__
                + ":  not an Angle"
            )
        return self.setDegrees(self.getDegrees() + angle.getDegrees())

    def subtract(self, angle):
        if type(angle) is not Angle:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.subtract.__name__
                + ":  not an Angle"
            )
        return self.setDegrees(self.getDegrees() - angle.getDegrees())

    def compare(self, angle):
        if type(angle) is not Angle:
            raise ValueError (
                self.__class__.__name__ + "."
                + self.compare.__name__
                + ":  not an Angle"
            )
        if self.getDegrees() > angle.getDegrees():
            return 1
        elif self.getDegrees() < angle.getDegrees():
            return -1
        else:
            return 0

    def getString(self):
        return ("%dd%.1f" % (int(self.getDegrees()),
            (self.getDegrees() % 1) * self.__minute))

    def getDegrees(self):
        return self.angle
