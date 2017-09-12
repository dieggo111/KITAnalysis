import sys, os
import numpy as np
# Ubuntu
# sys.path.append("/home/diego/KITPlot")
# Win10
sys.path.append("C:\\Users\\Marius\\KITPlot\\")
from KITPlot import KITData

class dataGrabber(object):

    def __init__(self):
        # Ubuntu
        # path = "/home/diego/KITPlot/"
        # Win10
        self.path = "C:\\Users\\Marius\\KITPlot\\"

        self.__IDList = []
        self.__dataList = []
        self.__searchList = []
        self.__paraList = ["Voltage","Annealing"]
        self.__default_gain = 210
        self.__annealing_norm = 1

    def main(self,runNr,searchItem,*args):

        self.search_n_collect(runNr,searchItem,*args)
        self.output()
        self.exportFile(*args)

        return self.__searchList

    # runNr must look like "startNr-endNr"
    # searchPara must look like "Para=Value"
    def search_n_collect(self,runNr,searchItem,*args):

        # check if default gain was set by user
        try:
            gain = [x for x in args if "gain" in x.lower()][0]
            gain = int(gain.split("=")[1])
        except:
            gain = None

        # validate input (must be "ID-ID") and determine search parameter
        try:
            (startNr,endNr) = runNr.split("-")
            (para,val) = searchItem.split("=")
            if para not in self.__paraList or val.isdigit() is False:
                raise ValueError("Unkown parameter")
            else:
                pass
        except:
            raise ValueError("Unkown input")

        if int(startNr) > int(endNr):
            raise ValueError("Unexpected input. StartNr must be smaller"
                             " than endNr!")
        else:
            pass

        # make ID list from ID to ID
        for i in range(int(startNr),(int(endNr)+1)):
            self.__IDList.append(int(i))

        # start search
        for ID in self.__IDList:
            try:
                self.__dataList.append(KITData(ID,measurement="alibava",show_input=False))
            except (ValueError) as e:
                sys.exit(e)
            except:
                pass

        if self.__dataList == []:
            raise ValueError("Can't find complete runs in between {0} and {1}".format(startNr,endNr))
        else:
            pass

        print("Search completed...")

        Name = self.__dataList[0].getName()

        # fill self.__searchList
        for kData in self.__dataList:
            if Name == kData.getName() and para == "Voltage":
                if int(val) in range(int(abs(round(kData.getX()[0]))-1),\
                                     int(abs(round(kData.getX()[0]))+2)) \
                                     and Name == kData.getName():
                    try:
                        # if it's an old Alibava measurement
                        if kData.getGain() == 1.0 and gain == None:
                            gain = self.__default_gain
                            seed = self.__default_gain*kData.getSeed()
                        else:
                            # if a default gain was given by user
                            try:
                                seed = gain*kData.getSeed()
                            # use gain from measurement calibration
                            except:
                                seed = kData.getGain()*kData.getSeed()

                        if kData.getGain() == seed/kData.getSeed():
                            self.__searchList.append((str(kData.getName()),
                                                      kData.getID(),
                                                      abs(round(kData.getX()[0])),
                                                      round(kData.getGain()),
                                                      round(kData.getZ()[0]/24),
                                                      round(seed)))
                            gain = None
                        else:
                            self.__searchList.append((str(kData.getName()),
                                                      kData.getID(),
                                                      abs(round(kData.getX()[0])),
                                                      round(gain),
                                                      round(kData.getZ()[0]/24),
                                                      round(seed)))
                    except:
                         pass
                else:
                    pass



            elif Name == kData.getName() and para == "Annealing":
                # print((int(val) in range(int(round(kData.getZ()[0]/24*0.8)),int(round(kData.getZ()[0]/24*1.1)))))
                if (int(val) in range(int(round(kData.getZ()[0]/self.__annealing_norm*0.8)),\
                                      int(round(kData.getZ()[0]/self.__annealing_norm*1.1))) \
                                      or int(val) == kData.getZ()[0])\
                                      and Name == kData.getName():
                    try:
                        # if it's an old Alibava measurement
                        if kData.getGain() == 1.0 and gain == None:
                            gain = self.__default_gain
                            seed = self.__default_gain*kData.getSeed()
                        else:
                            # if a default gain was given by user
                            try:
                                seed = gain*kData.getSeed()
                            # use gain from measurement calibration
                            except:
                                seed = kData.getGain()*kData.getSeed()
                        if kData.getGain() == seed/kData.getSeed():
                            self.__searchList.append((str(kData.getName()),
                                                      kData.getID(),
                                                      abs(round(kData.getX()[0])),
                                                      round(kData.getGain()),
                                                      round(kData.getZ()[0]/self.__annealing_norm),
                                                      round(seed)))
                            gain = None
                        else:
                            self.__searchList.append((str(kData.getName()),
                                                      kData.getID(),
                                                      abs(round(kData.getX()[0])),
                                                      round(gain),
                                                      round(kData.getZ()[0]/self.__annealing_norm),
                                                      round(seed)))
                    except:
                        pass
                else:
                    pass
            else:
                pass

        if self.__searchList == []:
            raise ValueError("Couldn't find data that met the requirements")


    def output(self):

        print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15}"\
              .format("SensorName","Run","Voltage","Gain","Annealing","SeedSignal"))
        for foo in self.__searchList:
            print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15}"\
                  .format(*foo))


    def exportFile(self,*args):

        try:
            expo = [x for x in args if "-as" in x.lower() or "-vs" in x.lower()][0]

            if expo == "-as":
                with open(self.path + str(self.__dataList[0].getName() + ".txt"), 'w') as File:
                    for line in self.__searchList:
                        File.write(str(line[4]) + "   " + str(line[5]) + "\n")
                File.close()
                print("Data written into %s" %(str(self.__dataList[0].getName() + ".txt")))
            elif expo == "-vs":
                with open(self.path + str(self.__dataList[0].getName() + ".txt"), 'w') as File:
                    for line in self.__searchList:
                        File.write(str(line[2]) + "   " + str(line[5]) + "\n")
                File.close()
                print ("Data written into %s" %(str(self.__dataList[0].getName() + ".txt")))
        except:
            pass


if __name__ == '__main__':

    d = dataGrabber()
    d.main(*sys.argv[1:])
    d.output()
