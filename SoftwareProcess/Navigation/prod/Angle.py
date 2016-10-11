"""
    September 10th 2016

    author: Jesse Gamez
"""

class Angle(object):
    __period = 360
    __minute = 60

    def __init__(self, degrees = 0):
        self.setDegrees(degrees)

    def setDegrees(self, degrees = 0):
        degrees = float(degrees)

        if degrees < 0:
            return self.setDegrees(degrees + self.__period)

        self.angle = degrees % self.__period

        return self.getDegrees()

    def setDegreesAndMinutes(self, degrees):
        degrees = degrees.split("d")

        if len(degrees) != 2:
            raise ValueError("missing separator")

        minutes = degrees[1].split(".")
        if len(minutes) != 2 or len(minutes[1]) > 1:
            raise ValueError("invalid minute precision")

        minutes = float(degrees[1])
        if minutes < 0:
            raise ValueError("minutes may not be negative")

        if degrees[0][0] == '-':
            minutes *= -1

    # degrees + minutes / minute
        return self.setDegrees(int(degrees[0]) + minutes / self.__minute)

    def add(self, angle):
        return self.setDegrees(self.getDegrees() + angle.getDegrees())

    def subtract(self, angle):
        return self.setDegrees(self.getDegrees() - angle.getDegrees())

    def compare(self, angle):
        if self.getDegrees() > angle.getDegrees():
            return 1
        elif self.getDegrees() < angle.getDegrees():
            return -1
        else:
            return 0

    def getString(self):
        return (str(int(self.getDegrees())) +
        "d" +
        str(round((self.getDegrees() % 1) * self.__minute, 1)))

    def getDegrees(self):
        return self.angle
