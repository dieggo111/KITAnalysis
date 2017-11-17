import os, sys
import numpy as np
# sys.path.append("/home/diego/KITPlot/")
sys.path.append("C:\\Users\\Marius\\KITPlot")
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

    def __init__(self,Input,limitDic):

        self.Input = Input
        self.fileList = []
        self.path = "/home/diego/Desktop/Data/HPK_2S_II_"
        self.sections = []

        self.cfgPath = "/home/diego/KITPlot/"

        self.limitDic = limitDic


    def init(self):

        # single ID
        if self.Input.isdigit() == True:
            file1 = KITData(self.Input)

            fileOutput = self.calc(file1)

            print("(" + str(len(file1.getY())-fileOutput[0]) + ") of ("
                  + str(len(file1.getY())) + ") data points excluded")
            print(str(file1.getName()) + "_" + str(file1.getParaY()) + " = "
                  + str(fileOutput[1]) + " ;   " + str(fileOutput[2]) + ";")
            return (file1,fileOutput)

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
                      + str(self.calc(self.fileList[i])[1]) + " +/- "
                      + str(self.calc(self.fileList[i])[2]))
            return self.fileList


    def calc(self,data):
        corrList=[]
        for val in data.getY():
            if self.limitDic[data.getParaY()][0]<abs(val)<self.limitDic[data.getParaY()][1]:
                corrList.append(val)
            else:
                pass

        mean = "{:0.3e}".format(np.mean(corrList))
        std = "{:0.3e}".format(np.std(corrList))

        return (len(corrList),mean,std)


    def write(self):
        for i, data in enumerate(self.fileList):
            with open(self.path + os.path.basename(self.Input), 'w') as File:
                for i, val in enumerate(self.fileList):
                    File.write("{:>15} {:>20} {:>20}".format(str(self.fileList[i].getParaY())+";",str(np.mean(self.fileList[i].getY()))+";",str(np.std(self.fileList[i].getY())))+";" +"\n")
            File.close()

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
