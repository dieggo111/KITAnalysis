import sys
import numpy as np
import ROOT 
sys.path.append('modules/')
import KITData
import KITPlot
import os, sys


Input=sys.argv[1]
fileList = []
path = "/home/metzler/Schreibtisch/Data/Streifenscans/DataFiles/"
sections = []
corrList=[]

#max_val=5e-12
#min_val=-5e-12
max_val=1e13
min_val=1e11
#max_val=1.2e-12
#min_val=0.5e-12
#max_val=2e6
#min_val=1e6
#max_val=-25e-12
#min_val=-45e-12


# single ID
if Input.isdigit() == True:
    file1 = KITData.KITData(Input)

    for val in file1.getY():
        if min_val<val<max_val:
            corrList.append(val)
    print str(file1.getName())+"_"+str(file1.getParaY())+" = "+str(np.mean(corrList)).replace(".",",")+" ;   "+str(np.std(corrList)).replace(".",",")+";"

# files with IDs 
elif Input[-4:] == ".txt":
    with open(Input) as inputFile:
        for line in inputFile:
            entry = line.split()
            if entry[0].isdigit():
                fileList.append(KITData.KITData(entry[0]))

    for i, data in enumerate(fileList):
        print str(fileList[i].getName())+"_"+str(fileList[i].getParaY())+" = "+str(np.mean(fileList[i].getY()))+" +/- "+str(np.std(fileList[i].getY()))

    with open(path + os.path.basename(Input), 'w') as File:
        for i, val in enumerate(fileList):
            File.write("{:>15} {:>20} {:>20}".format(str(fileList[i].getParaY())+";",str(np.mean(fileList[i].getY())).replace(".",",")+";",str(np.std(fileList[i].getY()))).replace(".",",")+";" +"\n")
        File.close()
else:
    print "?"



