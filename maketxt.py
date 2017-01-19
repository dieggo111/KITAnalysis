#!/usr/bin/python
import sys, os
import numpy as np
import ROOT 
sys.path.append('modules/')
from KITData import KITData
from KITPlot import KITPlot

path1 = sys.argv[1]
path2 = sys.argv[2]
writepath = "/home/metzler/Schreibtisch/Data/Fits/"
name = os.path.basename(sys.argv[1]).replace("_BSB","").replace("_FSB","")


V1=[]
V2=[]
BSB=[]
FSB=[]
V=[]
Temp=[]
Temp2=[]
Vstar=[]

with open (path1, 'r') as File:
    for line in File:
        if "BSB" in path1:
            V1.append(line.split()[0])
            BSB.append(float(line.split()[1].replace(",",".")))
        else:
            V2.append(line.split()[0])
            FSB.append(float(line.split()[1].replace(",",".")))

with open (path2, 'r') as File:
    for line in File:
        if "BSB" in path2:
            V1.append(line.split()[0])
            BSB.append(float(line.split()[1].replace(",",".")))
        else:
            V2.append(line.split()[0])
            FSB.append(float(line.split()[1].replace(",",".")))

# gleiche spannungswerte

if V1 == V2:
    pass
else:
    if len(V1)>len(V2):
        for i, val in enumerate(V1):
            if val in V2:
                V.append(val)
            else:
                pass

        for v in V:
            Temp2.append(BSB[abs(int(v))])
        BSB = Temp2
    else:
        for j, val in enumerate(V2):
            if val in V1:
                V.append(val)
            else:
                pass
        for v in V:
            Temp2.append(FSB[abs(int(v))])
        FSB = Temp2

# werte suchen

for j, val2 in enumerate(FSB):
    Vstar.append(0)

for i, val in enumerate(BSB[:3]):
    if i==0:
        pass
    else:
        for j, val2 in enumerate(FSB):
            if abs(val2)>0.95*abs(BSB[i]) and abs(val2)<1.05*abs(BSB[i]):
                Temp.append((j, abs(val2), abs(val2-BSB[i])))
            else:
                pass

        pos = 0
        minimum = 0
        for index, v, dif in Temp:
            if minimum == 0:
                pos = index
                minimum = dif
            elif minimum>dif:
                pos = index
                minimum = dif
            else:
                pass
        print (pos, minimum)
        Vstar[pos] = i


#print (len(V), len(Vstar), len(BSB), len(FSB))



with open (writepath+name, 'w') as File:
    for i, val in enumerate(V):
        if i==0:
            pass
        else:
            File.write("{:>5} {:>20} {:>20} {:>5}".format(val.replace(".",",")+";", str(BSB[i]).replace(".",",")+";", str(FSB[i]).replace(".",",")+";", str(Vstar[i]) +"\n"))
    File.close()



