#!/usr/bin/env python3

import sys, os
import numpy as np




def setFormat(path, fileName=None):
    """ Values in .txt file may be in german format that uses ',' instead of '.'
        to seperate decimals. This needs to be corrected.
    """

    Lines=[]
    if fileName==None:
        with open (path, 'r') as File:
            for line in File:
                Lines.append(line.replace(",","."))
        with open (path, 'w') as File:
            for line in Lines:
                if line == "":
                    pass
                else:
                    File.write(line)
    else:
        with open (path + fileName, 'r') as File:
            for line in File:
                Lines.append(line.replace(",","."))
        with open (path + fileName, 'w') as File:
            for line in Lines:
                if line == "":
                    pass
                else:
                    File.write(line)

    return True


def getLists(path,fileName=None):

    x=[]
    y=[]
    y2=[]
    t=[]
    if fileName == None:
        with open (path, 'r') as File:
            for line in File:
                x.append(float(line.split()[0]))
                y.append(float(line.split()[1]))
                y2.append(float(line.split()[2]))
                t.append(float(line.split()[3]))
    else:
        with open (path + fileName, 'r') as File:
            for line in File:
                x.append(float(line.split()[0]))
                y.append(float(line.split()[1]))
                y2.append(float(line.split()[2]))
                t.append(float(line.split()[3]))

    return (x, y, y2, t)


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


def T_rho(dataInput):

    rho = []
    T = []
    for inputFile in os.listdir(dataInput):
        if (os.path.splitext(inputFile)[1] == ".txt"):
            setFormat(dataInput,inputFile)
            Vdep, V, I, t = getLists(dataInput,inputFile)
            T.append(round(np.mean(t)))
            m, b = np.polyfit(V,I,1)
            rho.append(round(1/m*A/L))
        else:
            pass

    # print(*zip(T, rho))

    with open ("output.txt", 'w') as File:
        for tup in zip(T, rho):
            File.write(str(tup[0]) + "     " + str(tup[1]) + "\n")

    print("output.txt has been created")

    return True

def TB_R(dataInput):

    setFormat(dataInput)
    Iter, R, Vdep, T = getLists(dataInput)

    with open ("output.txt", 'w') as File:
        for tup in zip(Iter, R):
            File.write(str(tup[0]) + "     " + str(tup[1]) + "\n")

    print("output.txt has been created")

    return True

if __name__ == '__main__':

    # KIT_Test_01
    A = 0.455312
    L = 0.02

    # T_rho(sys.argv[1])
    TB_R(sys.argv[1])


    input()
