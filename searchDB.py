import sys,os
sys.path.append("C:\\Users\\Marius\\KITPlot\\")
from KITPlot import KITData

class searchDB(object):

    def __init__(self,ID=None,Name=None):

        db = {"host": "192.168.13.2",
              "database": "sample",
              "user": "abfrage",
              "passwd": "JtjTN9M4WpQr,29t"}

        print(db["host"])
        print(ID)


if __name__ == '__main__':

    searchDB(ID=34745)
