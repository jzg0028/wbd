"""
    October 5th 2016
    October 6th 2016

    author: Jesse Gamez
"""

class Fix(object):

    def __init__(self, name = "log.txt"):
        if name.count(".txt") == 0 or name[-5:] == ".txt":
            raise ValueError

    # must store name instead of FD to avoid zombie FD
        self.log = name
        f = open(name, "a")
        f.write("Start of log\n")
        f.close()

    def setSightingFile(self, name):
        if name.count(".xml") == 0 or name[-5:] == ".xml":
            raise ValueError

    # must store name instead of FD to avoid zombie FD
        self.sightings = name
        f = open(name, "a")
        f.close()

    def getSightings():
        pass
