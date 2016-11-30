from Navigation.prod.Angle import Angle
import re

class Coordinate(object):
    def __init__(self, latitude = '0d0.0', longitude = '0d0.0'):
        self.setDegreesAndMinutes(latitude, longitude)

    def setDegreesAndMinutes(self, latitude, longitude):
        if not re.compile (
            '^(?:0?0?0d0?0.0|' \
            + '[SN]0?(?:(?:(?:[1-8]\d|' \
            + '0?[1-9])d[0-5]?\d\.\d)|' \
            + '0?0d(?:[1-5]\d\.\d|' \
            + '0?[1-9]\.\d|' \
            + '0?0\.[1-9])))$'
        ).match(latitude):
            raise ValueError("Coordinate: bad latitude: " + latitude)
        self.latitude = latitude

        if not re.compile('^(?:[0-2]?\d?\d|3[0-5]\d)d(?:[0-5]?\d\.\d)$') \
            .match(longitude):
            raise ValueError("Coordinate: bad longitude: " + longitude)
        self.longitude = longitude

    def setDegrees(self, latitude, longitude):
        self.setLatitudeString(
            ('S' if latitude < 0 else 'N' if latitude > 0 else '')
            + Angle(latitude).getString().replace('-', ''))

        self.setLongitudeString(Angle(longitude).getString())

    def latitudeAngle(self):
        return Angle (
            Angle().setDegreesAndMinutes (
                self.latitude.replace('S', '-').replace('N', '')
            )
        )

    def longitudeAngle(self):
        return Angle (
            Angle().setDegreesAndMinutes (
                self.longitude
            )
        )
