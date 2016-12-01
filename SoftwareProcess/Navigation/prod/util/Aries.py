class Aries(object):

    def __init__(self, fname, date, hour):
        self.fname, self.date, self.hour = fname, date, hour

        self.gha1, self.gha2 = self.line()

    def line(self):
        with open(self.fname, 'r') as ariesFile:

            line = ariesFile.readline()
            while line:
                line = line.split('\t')

                if line[0] == self.date and line[1] == self.hour:
                    return (line[2][0:-1],
                        ariesFile.readline().split('\t')[2][0:-1])

                line = ariesFile.readline()

            raise ValueError (
                "date or hour too early: date: " + date + " hour: " + hour
            )
