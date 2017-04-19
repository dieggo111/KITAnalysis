import os, sys
import numpy as np
sys.path.append("/home/diego/KITPlot/")
from KITPlot import KITData


"""The strip_mean script calculates the mean value of strip parameters directly
from the IEKP database. You can either choose
    - a single probe ID
    - a .txt file containing probe IDs
as your 'Input' argument to calculate mean value and its standard error. For
adjusting those mean values you are able to set boundaries. Every data point
that is outside the given interval will be excluded from the calculation. You
can also choose to print the results in a seperate .txt-file with the 'write'
method.
"""

class strip_mean(object):

    def __init__(self,Input,min_val=None,max_val=None):

        self.Input = Input
        self.fileList = []
        self.path = "/home/diego/Desktop/Data/HPK_2S_II_"
        self.sections = []

        self.cfgPath = "/home/diego/KITPlot/"

        self.min_val_leak = 0.01e-9
        self.max_val_leak = 1e-9

        self.min_val_pin = 0
        self.max_val_pin = 5e-12

        # for 2 cm long strips
        self.min_val_cc = 50e-12
        self.max_val_cc = 70e-12

        # for 2 cm long strips
        self.min_val_cint = 0.6e-12
        self.max_val_cint = 1.1e-12

        self.min_val_poly = 1e5
        self.max_val_poly = 2.5e6

        self.min_val_rint = 1e8
        self.max_val_rint = 1e13

        if min_val is not None:
            self.min_val_user = float(min_val)
        else:
            self.min_val_user = None

        if max_val is not None:
            self.max_val_user = float(max_val)
        else:
            self.max_val_user = None


    def init(self):

        # single ID
        if self.Input.isdigit() == True:
            file1 = KITData(self.Input)

            fileOutput = self.calc(file1,self.min_val_user,self.max_val_user)

            print("(" + str(len(file1.getY())-fileOutput[0]) + ") of ("
                  + str(len(file1.getY())) + ") data points excluded")
            print(str(file1.getName()) + "_" + str(file1.getParaY()) + " = "
                  + str(fileOutput[1]) + " ;   " + str(fileOutput[2]) + ";")

        # files with IDs
        elif self.Input[-4:] == ".txt":
            with open(self.Input) as inputFile:
                for line in inputFile:
                    entry = line.split()
                    if entry[0].isdigit():
                        self.fileList.append(KITData(entry[0]))

            for i, data in enumerate(self.fileList):
                print(str(self.fileList[i].getName()) + "_"
                      + str(self.fileList[i].getParaY()) + " = "
                      + str(np.mean(self.fileList[i].getY())) + " +/- "
                      + str(np.std(self.fileList[i].getY())))

        return True


    def calc(self,Data,min_val=None,max_val=None):

        corrList=[]

        if min_val is not None and max_val is not None:
            for val in Data.getY():
                if min_val<val<max_val:
                    corrList.append(val)
                else:
                    pass
            if corrList == []:
                raise ValueError("No data points within given interval!")
            else:
                pass
        elif min_val is None and max_val is None:
            for val in Data.getY():
                if "I_leak" in Data.getParaY():
                    if self.min_val_leak<abs(val)<self.max_val_leak:
                        corrList.append(val)
                    else:
                        pass
                elif "Pinhole" in Data.getParaY():
                    if self.min_val_pin<abs(val)<self.max_val_pin:
                        corrList.append(abs(val))
                    else:
                        pass
                elif "CC" in Data.getParaY():
                    if "Irradiation" in Data.getName() or "PCommon" in Data.getName():
                        if self.min_val_cc<val<self.max_val_cc:
                            corrList.append(val)
                        else:
                            pass
                    elif "KIT_Test" in Data.getName():
                        if self.min_val_cc/2<val<self.max_val_cc/2:
                            corrList.append(val)
                        else:
                            pass
                    else:
                        raise ValueError("Unkown sensor. Need boundaries as "
                                         "second and third argument...")
                elif "C_int" in Data.getParaY():
                    if "Irradiation" in Data.getName() or "PCommon" in Data.getName():
                        if self.min_val_cint<val<self.max_val_cint:
                            corrList.append(val)
                        else:
                            pass
                    elif "KIT_Test" in Data.getName():
                        if self.min_val_cint/2<val<self.max_val_cint/2:
                            corrList.append(val)
                        else:
                            pass
                    else:
                        raise ValueError("Unkown sensor. Need boundaries as "
                                         "second and third argument...")
                elif "R_poly" in Data.getParaY():
                    if self.min_val_poly<val<self.max_val_poly:
                        corrList.append(val)
                    else:
                        pass
                elif "R_int" in Data.getParaY():
                    if self.min_val_rint<val<self.max_val_rint:
                        corrList.append(val)
                    else:
                        pass

        mean = np.mean(corrList)
        std = np.std(corrList)

        return (len(corrList),mean,std)


    def write(self):
        for i, data in enumerate(self.fileList):
            with open(self.path + os.path.basename(self.Input), 'w') as File:
                for i, val in enumerate(self.fileList):
                    File.write("{:>15} {:>20} {:>20}".format(str(self.fileList[i].getParaY())+";",str(np.mean(self.fileList[i].getY()))+";",str(np.std(self.fileList[i].getY())))+";" +"\n")
            File.close()
        else:
            print("?")

        return True




# main loop
if __name__=='__main__':

    if len(sys.argv) is 2:
        s = strip_mean(sys.argv[1])
    elif len(sys.argv) is 4:
        s = strip_mean(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        raise ValueError("Missing Arguments")

    s.init()
