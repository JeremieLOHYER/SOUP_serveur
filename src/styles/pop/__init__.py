import os

import numpy
import reader
from styles.ServerTemplate import ServerTemplate


def getSongs():
    list = os.listdir('./')
    retList = []
    for object in list:
        if not object.__contains__(".py"):
            retList.append(object)
    return retList

def readSong(song):
    return True

if __name__ == '__main__':
    print(getSongs())

    readSong("./chipichipi.mp3")