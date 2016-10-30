class Aries(object):

    def __init__(self, fname, date, hour):
        line = self.search(fname, date, hour)

        if line == None:
            raise ValueError (
                "date or hour too early: date: " + date + "hour: " + hour
            )

        self.gha = line[2][0:-1]

    def search(self, fname, date, hour):
        with open(fname, 'r') as ariesFile:

            for line in ariesFile:
                line = line.split('\t')

                if line[0] == date and line[1] == hour:
                    return line

            return None
