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

class StripMean(object):

    def __init__(self):

        self.file_lst = []
        self.path = "/home/diego/Desktop/Data/HPK_2S_II_"
        self.sections = []

        self.cfgPath = "/home/diego/KITPlot/"

    def get_mean(self, data, para, limit_dic):
        """Calculates mean value and std deviation of data.
        """
        # dict with raw data
        if isinstance(data, dict):
            if "Ramp" in para:
                for key, val in data.items():
                    return self.calc(val, limit_dic, para)
            fileOutput = self.calc(data["dataY"],limit_dic, data["paraY"])
            r = round(float(fileOutput[0])*100,2)
            print("(" + str(r) + "%) of ("
                  + str(len(data["dataY"])) + ") data points excluded")
            print(str(data["name"]) + "_" + str(data["paraY"]) + " = "
                  + str(fileOutput[1]) + " ;   " + str(fileOutput[2]) + ";")
            return fileOutput

        # single ID
        elif data.isdigit() == True:
            file1 = KITData(data)

            fileOutput = self.calc(file1, limit_dic)
            r = round(float(fileOutput[0])*100,2)
            print("(" + str(r) + "%) of ("
                  + str(len(file1.getY())) + ") data points excluded")
            print(str(file1.getName()) + "_" + str(file1.getParaY()) + " = "
                  + str(fileOutput[1]) + " ;   " + str(fileOutput[2]) + ";")
            return fileOutput

        # files with IDs
        elif data[-4:] == ".txt":
            with open(data) as inputFile:
                for line in inputFile:
                    entry = line.split()
                    if entry[0].isdigit():
                        self.file_lst.append(KITData(entry[0]))
            for i, _ in enumerate(self.file_lst):
                print(str(self.file_lst[i].getName()) + "_"
                      + str(self.file_lst[i].getParaY()) + " = "
                      + str(self.calc(self.file_lst[i], limit_dic)[1]) + " +/- "
                      + str(self.calc(self.file_lst[i], limit_dic)[2]))
            return self.file_lst


    def calc(self, data, limit_dic, para=None):
        corr_lst = []
        if isinstance(data, KITData):
            for val in data.getY():
                if limit_dic[data.getParaY()][0] < abs(val) < \
                        limit_dic[data.getParaY()][1]:
                    corr_lst.append(val)
                else:
                    pass
            ratio = round(len(corr_lst)/len(data.getParaY()), 2)
        else:
            for val in data:
                try:
                    if limit_dic[para][0] < abs(val) < limit_dic[para][1]:
                        corr_lst.append(val)
                except:
                    corr_lst.append(val)
            ratio = round((len(data)-len(corr_lst))/len(data), 2)
        mean = "{:0.3e}".format(np.mean(corr_lst))
        std = "{:0.3e}".format(np.std(corr_lst))
        return (str(ratio), mean, std)

    def write(self):
        for i, data in enumerate(self.file_lst):
            with open(self.path + os.path.basename(self.data), 'w') as File:
                for i, val in enumerate(self.file_lst):
                    File.write("{:>15} {:>20} {:>20}".format(str(self.file_lst[i].getParaY())+";",str(np.mean(self.file_lst[i].getY()))+";",str(np.std(self.file_lst[i].getY())))+";" +"\n")
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
