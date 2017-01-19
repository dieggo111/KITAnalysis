import sys, os
import numpy as np
import ROOT 
sys.path.append('modules/')
from KITData import KITData


########################
x_para = "annealing_days"
#x_para = "annealing_hours"   
#x_para = "voltage"     
########################


# print information of single ID
if sys.argv[1].isdigit():

    kData = KITData(sys.argv[1],measurement="alibava")

    print "{:>15} {:>20}".format("Name:" , kData.getName())
    print "{:>15} {:>20}".format("Voltage:" , str(kData.getX()))
#    print "{:>15} {:>20}".format("Fluence:" , str(kData.getFluenceP()))
    print "{:>15} {:>20}".format("Annealing (hours):" , str(kData.getZ()))
    print "{:>15} {:>20}".format("Annealing (days):" , str(kData.getZ()[0]/24))
    if kData.getGain() == 1.0 or kData.getGain() == None:
        print "{:>15} {:>20}".format("Gain:" , str(220))
    else:
        print "{:>15} {:>20}".format("Gain:" , str(kData.getGain()))
    print "{:>15} {:>20}".format("Seed (ADC):" , str(kData.getSeed()))
    if kData.getGain() == 1.0 or kData.getGain() == None:
        print "{:>15} {:>20}".format("Seed err (e):" , str(220*kData.getSeederr()))
        print "{:>15} {:>20}".format("Seed (e):" , str(220*kData.getSeed()))
    else:
        print "{:>15} {:>20}".format("Seed err (e):" , str(kData.getGain()*kData.getSeederr()))
        print "{:>15} {:>20}".format("Seed (e):" , str(kData.getGain()*kData.getSeed()))



    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        print "{:>15} {:>20}".format("Seed* (e):" , str(int(sys.argv[2])*kData.getSeed()))
        print "{:>15} {:>20}".format("Seed err* (e):" , str(int(sys.argv[2])*kData.getSeederr()))


# print information of ID list into file
elif sys.argv[1].isdigit() == False and os.path.exists(sys.argv[1]):
    path = os.path.dirname(sys.argv[1]) + "/"

    with open(sys.argv[1], 'r') as inputFile:
        kDataList = []
        for ID in inputFile:
            ID = ID.replace("\n","")
            try :
                kDataList.append(KITData(ID,measurement="alibava"))
            except:
                print "Couldn't find run " + str(ID) + " in Database"
        inputFile.close()

    with open(path + kDataList[0].getName() + "_Seed.txt", 'w') as File:
        for kData in kDataList:
            # use fixed gain mode and voltage as x parameter
            if len(sys.argv) > 2 and sys.argv[2].isdigit() and x_para == "voltage":
                File.write("{:>0} {:>10} {:>10}".format(str(kData.getX()).replace("[","").replace("]","").replace("-","") , str(round(float(str(int(sys.argv[2])*kData.getSeed())))) , "800" +"\n"))
            # use gain from db and voltage as x parameter
            elif len(sys.argv) == 2 and x_para == "voltage":
                File.write("{:>0} {:>10} {:>10}".format(str(kData.getX()).replace("[","").replace("]","").replace("-","") , str(round(float(str(kData.getGain()*kData.getSeed())))) , "800" +"\n"))
            # use fixed gain mode and annealing as x parameter
            elif len(sys.argv) > 2 and sys.argv[2].isdigit() and x_para == "annealing_hours":
                File.write("{:>0} {:>10} {:>10}".format(str(round(float(kData.getZ()[0]))) , str(round(float(str(int(sys.argv[2])*kData.getSeed())))) , "800" +"\n"))
            elif len(sys.argv) > 2 and sys.argv[2].isdigit() and x_para == "annealing_days":
                File.write("{:>0} {:>10} {:>10}".format(str(round(float(kData.getZ()[0])/24)) , str(round(float(str(int(sys.argv[2])*kData.getSeed())))) , "800" +"\n"))
            # use gain from db and annealing as x parameter
            elif len(sys.argv) == 2 and x_para == "annealing_hours":
                File.write("{:>0} {:>10} {:>10}".format(str(round(float(kData.getZ()[0]))) , str(round(float(str(kData.getGain()*kData.getSeed())))) , "800" +"\n"))
            elif len(sys.argv) == 2 and x_para == "annealing_days":
                File.write("{:>0} {:>10} {:>10}".format(str(round(float(kData.getZ()[0])/24)) , str(round(float(str(kData.getGain()*kData.getSeed())))) , "800" +"\n"))
            else:
                sys.exit("Don't know what to do...")
        File.close()

    print "'Voltage / Seed (e) was written in: " + path + kDataList[0].getName() + "_Seed.txt"

else:
    sys.exit("Input can not be identified")




raw_input()
