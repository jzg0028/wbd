class Star(object):

    def __init__(self, fname, body, date):
        line = self.floor(fname, body, date)
        if line == None:
            raise ValueError("observed date too early")

        self.declination = line[3][0:-1]
        self.hda = line[2]

    def floor(self, fname, body, date):
        with open(fname, 'r') as starFile:
        # search for the floor of dates for the given body
        # in an ascending list of values,
        # the greatest value that's less or equal to than the key,
        # is the value before the first value that's greater than the key
            prevline = None
            for line in starFile:
                line = line.split('\t')

            # search for first date that's greater than the given date
                if line[1] > date:
                    return prevline

            # save last line that had same body
                if line[0] == body:
                    prevline = line

            return prevline
