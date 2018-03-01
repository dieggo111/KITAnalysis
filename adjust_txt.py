#!/usr/bin/python
import sys, os
import numpy as np


path = "C:\\Users\\Marius\\KITPlot\\Data\\RelayTest\\Sensor\\Ileak\\Ileak_RUN238_RelayTest_Ramp_1.txt"

# turn "," into "."
# for folder in os.listdir(path):
#     for dFile in os.listdir(os.path.join(path,folder)):
#         with open (os.path.join(path,folder,dFile), 'r') as File:
#             temp = []
#             for line in File:
#                 temp.append(line.replace(",","."))
#             File.close()
#         with open (os.path.join(path,folder,dFile), 'w') as File:
#             for line in temp:
#                 File.write(line)
#             File.close()

# # change first column in file
# for dFile in os.listdir(path):
with open (path, 'r') as File:
    temp = []
    i=0
    for line in File:
        temp.append(line.replace("1.000000E+0",str(i)))
        i+=10
    File.close()
with open (path, 'w') as File:
    for line in temp:
        File.write(line)
    File.close()



            # 2.100000E+1
        #     temp = []
        #     # print(dFile)
        #     for line in File:
        #         # print(line, type(line.split()))
        #         splitted = line.split()
        #         # print(splitted)
        #         splitted.extend(["0","1000"])
        #         temp.append(splitted)
        #
        # with open (path+dFile, 'w') as File:
        #     for line in temp:
        #             File.write("{:<5} {:<10} {:<10} {:<10}".format(line[0], line[1], line[2], line[3]+"\n"))
