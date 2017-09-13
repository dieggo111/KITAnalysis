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
        self.defaultPath = "C:\\Users\\Marius\\KITPlot\\"

        self.__dataList = []
        self.__searchList = []
        self.__paraList = ["Voltage","Annealing"]
        self.__default_gain = 210
        self.__annealing_norm = 1

    def main(self,runNr,searchItem,*args):

        self.search_n_collect(runNr,searchItem,*args)
        self.output()

        return self.__searchList


    def search_n_collect(self,runNr,searchItem,*args):
        """
        runNr must look like "startNr-endNr"
        searchPara must look like "Para=Value"

        """
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

        # fill self.__dataList with kitdata files
        self.fill_dataList(startNr,endNr)

        if self.__dataList == []:
            raise ValueError("Can't find complete runs in between {0} and {1}".format(startNr,endNr))
        else:
            pass

        print("Search completed...")

        # check if default name was set by user
        try:
            gain = [x for x in args if "gain" in x.lower()][0]
            gain = int(gain.split("=")[1])
        except:
            gain = None

        # check if sensor name was given by user
        try:
            name = [x for x in args if "name" in x.lower()][0]
            name = name.split("=")[1]
        except:
            name = self.__dataList[0].getName()

        # fill self.__searchList
        for kData in self.__dataList:
            if name == kData.getName() and para == "Voltage":
                if int(val) in range(int(abs(round(kData.getX()[0]))-1),\
                                     int(abs(round(kData.getX()[0]))+2)):
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
                            self.__searchList.append({"Name" :          str(kData.getName()),
                                                       "ID" :           str(kData.getID()),
                                                       "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                       "Gain" :         str(round(kData.getGain())),
                                                       "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                       "Seed" :         str(round(seed))})
                            gain = None
                        else:
                            self.__searchList.append({"Name" :          str(kData.getName()),
                                                       "ID" :           str(kData.getID()),
                                                       "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                       "Gain" :         str(round(gain)),
                                                       "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                       "Seed" :         str(round(seed))})
                    except:
                         pass
                else:
                    pass

            elif name == kData.getName() and para == "Annealing":
                # print((int(val) in range(int(round(kData.getZ()[0]/24*0.8)),int(round(kData.getZ()[0]/24*1.1)))))
                if (int(val) in range(int(round(kData.getZ()[0]/self.__annealing_norm*0.8)),\
                                      int(round(kData.getZ()[0]/self.__annealing_norm*1.1))) \
                                      or int(val) == kData.getZ()[0]):
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
                            self.__searchList.append({"Name" :          str(kData.getName()),
                                                       "ID" :           str(kData.getID()),
                                                       "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                       "Gain" :         str(round(kData.getGain())),
                                                       "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                       "Seed" :         str(round(seed))})
                            gain = None
                        else:
                            self.__searchList.append({"Name" :          str(kData.getName()),
                                                       "ID" :           str(kData.getID()),
                                                       "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                       "Gain" :         str(round(gain)),
                                                       "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                       "Seed" :         str(round(seed))})
                    except:
                        pass
                else:
                    pass
            else:
                pass

        if self.__searchList == []:
            raise ValueError("Couldn't find data that met the requirements")

        return True


    def output(self):

        print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15}"\
              .format("SensorName","Run","Voltage","Gain","Annealing","SeedSignal"))
        for foo in self.__searchList:
            print("{:<20} {:<15} {:<15} {:<15} {:<15} {:<15}"\
                  .format(*list(foo.values())))

        return True


    def exportFile(self,searchList,para,path=None):

        # Ubuntu
        # path = "/home/diego/KITPlot/"
        # Win10
        if path == None or path == "":
            path = self.defaultPath
        else:
            pass

        if not os.path.exists(path):
            raise ValueError("Given path does not exist.")

        try:
            if para == "Voltage":
                with open(path + searchList[0]["Name"] + ".txt", 'w') as File:
                    for dic in searchList:
                        File.write("{:<15} {:<15}".format(dic["Annealing"], dic["Seed"]) + "\n")
                File.close()
                print("Data written into %s" %(searchList[0]["Name"] + ".txt"))
            elif para == "Annealing":
                with open(path + searchList[0]["Name"] + ".txt", 'w') as File:
                    for line in searchList:
                        File.write("{:<15} {:<15}".format(dic["Voltage"], dic["Seed"]) + "\n")
                File.close()
                print ("Data written into %s" %(searchList[0]["Name"] + ".txt"))
        except:
            pass

        return True

    def fill_dataList(self,startNr,endNr):

        # make ID list from ID to ID
        IDList = range(int(startNr),int(endNr)+1)

        # start search
        for ID in IDList:
            try:
                self.__dataList.append(KITData(ID,measurement="alibava",show_input=False))
            except (ValueError) as e:
                sys.exit(e)
            except:
                pass

        return True



if __name__ == '__main__':

    d = dataGrabber()
    d.main(*sys.argv[1:])
    d.output()
