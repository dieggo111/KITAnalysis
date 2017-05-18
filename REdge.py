#!/usr/bin/env python3

import sys, os
import numpy as np
import ROOT
sys.path.append("/home/diego/KITPlot/")
from KITPlot import KITData
from KITPlot import KITPlot



def setFormat(path):
    """ Values in .txt file may be in german format that uses ',' instead of '.'
        to seperate decimals. This needs to be corrected.
    """

    Lines=[]
    with open (path, 'r') as File:
        for line in File:
            Lines.append(line.replace(",","."))
    with open (path, 'w') as File:
        for line in Lines:
            if line == "":
                pass
            else:
                File.write(line)
    return True


def getLists(path):

    x=[]
    y=[]
    y2=[]
    with open (path, 'r') as File:
        for line in File:
            x.append(abs(float(line.split()[0])))
            y.append(abs(float(line.split()[1])))
            y2.append(abs(float(line.split()[2])))
    return (x, y, y2)


def average(List, minimum=None, maximum=None):

    TempList=[]

    if minimum is not None and maximum is not None:
        if type(minimum) is int or type(maximum) == int:
            for val in List:
                if minimum<=val<=maximum:
                    TempList.append(val)
                else:
                    pass
        else:
            sys.exit("Unexpected boarders!!!")

        return np.mean(TempList)
    else:
        return np.mean(List)


def straighten(path):

    """ Some values in the .txt files may be corrupted due to bugs of the
        measurement device. These values need to be deleted.
    """

    Lines=[]
    I=[]
    LV=[]
    delList=[]
    with open (path, 'r') as File:
        for line in File:
            I.append(float(line.split()[2]))
            Lines.append(line.replace(",","."))
            LV.append(float(line.split()[1]))

    if "_for_" in path:
        for i, val in enumerate(I):
            if i==0 and abs(I[0]) > abs(I[1]):
                delList.append(i)
            elif i==len(I)-1:
                pass
            elif LV[i] == 0 and abs(I[i]) > abs(I[i+1]):
                delList.append(i)
            else:
                pass

    if "_rev_" in path:
        for i, val in enumerate(I):
            if i==0 and I[0] < I[1]:
                delList.append(i)
            elif i==len(I)-1:
                pass
            elif LV[i] == min(LV) and I[i] < I[i+1]:
                delList.append(i)
            else:
                pass

    with open (path, 'w') as File:
        for i, line in enumerate(Lines):
            if i in delList:
                pass
            else:
                File.write(line)

    return True




if __name__ == '__main__':

###################
    Redge = True #
###################

    setFormat(sys.argv[1])

    # Ramp measurements
    if Redge == True:

        straighten(sys.argv[1])

        kPlot1 = KITPlot(sys.argv[1])
        kPlot1.draw("APL")

        v = kPlot1.interpolate()
        R = []
        for name, val in v:
            R.append((name, 1/val))

        print("\n" + "Resistances:" + "\n")
        for pair in R:
            name, val = pair
            print("{:>8} {:>15}".format(name+": ", str(np.round(val))))

    # IV Diff
    else:
        Vfit=[]
        Vedge=[]
        tempY=[]
        tempX=[]
        x,y,y2 = getLists(sys.argv[1])
        lower=0
        for i, val2 in enumerate(y2):
            if min(y)>=val2:
                start = i+1
            elif i >= start:
                for j, val in enumerate(y):
                    if val<val2:
                        lower = j
                j = 0
                while y[j]<val2:
                    j+=1
                upper = j

                tempX.append(x[lower])
                tempX.append(x[upper])
                tempY.append(y[lower])
                tempY.append(y[upper])
                v = kPlot1.interpolate(tempY,tempX)
                del tempX[:]
                del tempY[:]

                V = v[0][0]*val2+v[0][1]
                Vfit.append((val2, V, x[i]-V))
                Vedge.append(x[i]-V)

        for triplet in Vfit:
            e, f, g = triplet
            print("{:>15} {:>15} {:>15}".format(str(e).replace(".",",")+" ; ", str(np.round(f,2)).replace(".",",")+" ; ", str(np.round(g,2)).replace(".",",")))
        print("\n" + "V_edge: " + str(np.round(average(Vedge), 2)))



    input()
