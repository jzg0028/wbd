from Navigation.prod.Angle import Angle

class Coordinate(object):
    def __init__(self, latitude, longitude):
        if type(latitude) is Angle and type(longitude) is Angle:
            self.setByAngle(latitude, longitude)
        elif type(latitude) is str and type(longitude) is str:
            self.setByString(latitude, longitude)
        else:
            self.setByDegree(latitude, longitude)
    
    def latStr(self):
        return (('' if self.lat % 90 == 0 else
        'N' if self.lat > 0 else 'S')
        + ("%dd%.1f" % (int(abs(self.lat) % 90),
        (self.lat % 1) * 60)))

    def lonStr(self):
        return Angle(self.lon).getString()

    def setByString(self, latitude, longitude):
        self.setByDegree (
            Angle(latitude.replace('S', '-').replace('N', '')).angle,
            Angle(longitude).angle
        )

    def setByAngle(self, latitude, longitude):
        self.setByDegree (
            latitude.angle,
            longitude.angle
        )

    def setByDegree(self, latitude, longitude):
        self.lat, self.lon = latitude, longitude
