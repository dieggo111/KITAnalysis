import sys, os
import numpy as np
from pathlib import Path
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, str(Path(os.getcwd()).parents[0]))
from KITPlot.KITSearch import KITSearch

class dataGrabber(object):

    def __init__(self,credentials):

        self.__dataList = []
        self.__searchList = []
        self.__paraList = ["Voltage","Annealing"]
        self.__default_gain = 210
        self.__annealing_norm = 1
        self.dbCreds = credentials

    def strip_search(self,name,project,para):
        session = KITSearch(self.dbCreds)
        dic = session.probe_search_for_name(name,project)
        if para == "*":
            # get rid of unanalyzed sections
            dic = self.pop_items(dic,"IVCV")
            # KITAnalysis expects values to be str type
            dic = self.convert_keys(dic)
        else:
            dic = self.pop_items(dic,para)
            dic = self.convert_keys(dic)
        return dic

    def alibava_search(self,name,project,para,value):
        session = KITSearch(self.dbCreds)
        if para == "Voltage":
            dic = session.ali_search_for_name_voltage(name,int(value),project)
            # get rid of unanalyzed sections
            dic = self.pop_items(dic,"unanalyzed")
            # KITAnalysis expects values to be str type
            dic = self.convert_keys(dic)
        elif para == "Annealing":
            dic = session.ali_search_for_name_annealing(name,int(value),project)
            dic = self.pop_items(dic)
            dic = self.convert_keys(dic)
        return dic

    def convert_keys(self,dic):
        for sec in dic:
            for sub in dic[sec]:
                if isinstance(dic[sec][sub], (int, float)):
                    dic[sec][sub] = str(abs(round(dic[sec][sub])))
        return dic

    def pop_items(self,dic,opt):
        delList = []
        for sec in dic:
            if opt == "unanalyzed" and dic[sec]["gain"] == None:
                delList.append(sec)
            elif opt == "IVCV" and dic[sec]["paraY"] in ("C_tot", "I_tot"):
                delList.append(sec)
            elif opt in ("R_int","R_poly_dc","I_leak_dc","C_int","CC","Pinhole") and dic[sec]["paraY"] != opt:
                delList.append(sec)
        for run in delList:
            dic.pop(run)
        return dic

    def output(self):

        print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"\
              .format("SensorName","Project","Run","Voltage","Gain","Annealing","SeedSignal"))
        for foo in self.__searchList:
            print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"\
                  .format(*list(foo.values())))

        return True

if __name__ == '__main__':

    d = dataGrabber()
    d.name_search_ali("Irradiation_04")
