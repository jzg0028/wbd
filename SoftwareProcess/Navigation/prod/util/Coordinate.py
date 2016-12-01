from Navigation.prod.Angle import Angle
import re

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
        if not re.compile (
            '^(0?0?0d0?0\.0|' \
            + '[NS]0?(([1-8]\d|' \
            + '0?[1-9])d(\d?\d\.\d)|'
            + '0?0?0d([1-5]\d\.\d|'
            + '0?[1-9]\.\d|'
            + '0?0\.[1-9])))$'
        ).match(latitude):
            raise ValueError('Coordinate: bad latitude: ' + latitude)
        if not re.compile('^([0-2]?\d?\d|3[0-5]\d)d[0-5]?\d\.\d$') \
            .match(longitude):
            raise ValueError('Coordinate: bad longitude: ' + longitude)

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
