import sys, os
import numpy as np
from pathlib import Path
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, str(Path(os.getcwd()).parents[0]))
from KITPlot.KITSearch import KITSearch

class dataGrabber(object):

    def __init__(self):

        self.__dataList = []
        self.__searchList = []
        self.__paraList = ["Voltage","Annealing"]
        self.__default_gain = 210
        self.__annealing_norm = 1

        self.db = {   "host": "192.168.13.2",
                      "port": "3306",
                      "database": "sample",
                      "user": "abfrage",
                      "passwd": "JtjTN9M4WpQr,29t"}

    def output(self):

        print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"\
              .format("SensorName","Project","Run","Voltage","Gain","Annealing","SeedSignal"))
        for foo in self.__searchList:
            print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"\
                  .format(*list(foo.values())))

        return True


    def alibava_search(self,name,para,value):
        session = KITSearch(self.db)
        if para == "Voltage":
            dic = session.search_for_name_voltage(name,int(value),"alibava")
            # KITAnalysis expects values to be str type
            for sec in dic:
                for sub in dic[sec]:
                    if isinstance(dic[sec][sub], (int, float)):
                        dic[sec][sub] = str(round(dic[sec][sub]))
            return dic
        elif para == "Annealing":
            pass


if __name__ == '__main__':

    d = dataGrabber()
    d.name_search_ali("Irradiation_04")
