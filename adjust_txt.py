#!/usr/bin/python
import sys, os
import numpy as np


path = "C:\\Users\\Marius\\KITPlot\\Data\\HPK_2S_II\\Signal_vs_Annealing_new\\"

for dFile in os.listdir(path):
    with open (path+dFile, 'r') as File:
        temp = []
        # print(dFile)
        for line in File:
            # print(line, type(line.split()))
            splitted = line.split()
            # print(splitted)
            splitted.extend(["0","1000"])
            temp.append(splitted)
        print(temp)

    with open (path+dFile, 'w') as File:
        for line in temp:
                File.write("{:<5} {:<10} {:<10} {:<10}".format(line[0], line[1], line[2], line[3]+"\n"))
