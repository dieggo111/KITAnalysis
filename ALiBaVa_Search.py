import sys, os
import numpy as np
sys.path.append("/home/diego/KITPlot/modules")
from KITData import KITData

cfgPath = "/home/diego/KITPlot/"
IDList = []
dataList = []
searchList = []
paraList = ["Voltage","Annealing"]

# validate input (must be "ID-ID") and determine search parameter

try:
    (x,y) = sys.argv[1].split("-")
    (para,val) = sys.argv[2].split("=")
    if para not in paraList or val.isdigit() is False:
        raise ValueError("Unkown parameter")
    else:
        pass
except:
    raise ValueError("Unkown input")

if int(x) > int(y):
    raise ValueError("Wrong input. Try 'min(ID),max(ID)'")
else:
    pass

# make ID list from ID to ID
for i in range(int(x),(int(y)+1)):
    IDList.append(int(i))

# start search
for ID in IDList:
    try:
        dataList.append(KITData(ID,measurement="alibava",db=cfgPath,show_input="False"))
    except (ValueError) as e:
        sys.exit(e)
    except:
        pass

if dataList == []:
    raise ValueError("Can't find complete runs in between {0} and [1}".format(x,y))
else:
    pass

print("Search completed...")

Name = dataList[0].getName()

# check if search value is satisfied
for kData in dataList:
    if Name == kData.getName() and para == "Voltage":
        for volt in kData.getX():
            if int(val) in range(int(abs(round(volt))-1),int(abs(round(volt))+2)) and Name == kData.getName():
                try:
                    if kData.getGain() == 1.0:
                        Seed = 220*kData.getSeed()
                    else:
                        Seed = kData.getGain()*kData.getSeed()
                    searchList.append((str(kData.getName()),kData.getID(),abs(round(volt)),round(kData.getZ()[0]/24),round(Seed)))
                except:
                     pass
            else:
                pass

    elif Name == kData.getName() and para == "Annealing":
        if int(val) in range(int(abs(round(kData.getZ()[0]/24*0.8))),int(abs(round(kData.getZ()[0]/24*1.1)))) and Name == kData.getName():
            try:
                if kData.getGain() == 1.0:
                    Seed = 220*kData.getSeed()
                else:
                    Seed = kData.getGain()*kData.getSeed()
                searchList.append((str(kData.getName()),kData.getID(),abs(round(kData.getX()[0])),round(kData.getZ()[0]/24),round(Seed)))
            except:
                pass
        else:
            pass
    else:
        pass


if searchList == []:
    raise ValueError("Couldn't find data that met the requirements")
else:
    for foo in searchList:
        print(foo)


path = os.getcwd() + "/"
try:
    if sys.argv[3] == "-as":
        with open(path + str(dataList[0].getName() + ".txt"), 'w') as File:
            for line in searchList:
                File.write(str(line[3]) + "   " + str(line[4]) + "\n")
        File.close()
        print("Data written into %s") %(str(dataList[0].getName() + ".txt"))
    elif sys.argv[3] == "-vs":
        with open(path + str(dataList[0].getName() + ".txt"), 'w') as File:
            for line in searchList:
                File.write(str(line[2]) + "   " + str(line[4]) + "\n")
        File.close()
        print ("Data written into %s") %(str(dataList[0].getName() + ".txt"))
except:
    pass



#    kData = KITData(sys.argv[1],measurement="alibava")

#    print "{:>15} {:>20}".format("Name:" , kData.getName())
#    print "{:>15} {:>20}".format("Voltage:" , str(kData.getX()))
##    print "{:>15} {:>20}".format("Fluence:" , str(kData.getFluenceP()))
#    print "{:>15} {:>20}".format("Annealing (hours):" , str(kData.getZ()))
#    print "{:>15} {:>20}".format("Annealing (days):" , str(kData.getZ()[0]/24))
#    if kData.getGain() == 1.0 or kData.getGain() == None:
#        print "{:>15} {:>20}".format("Gain:" , str(220))
#    else:
#        print "{:>15} {:>20}".format("Gain:" , str(kData.getGain()))
#    print "{:>15} {:>20}".format("Seed (ADC):" , str(kData.getSeed()))
#    if kData.getGain() == 1.0 or kData.getGain() == None:
#        print "{:>15} {:>20}".format("Seed err (e):" , str(220*kData.getSeederr()))
#        print "{:>15} {:>20}".format("Seed (e):" , str(220*kData.getSeed()))
#    else:
#        print "{:>15} {:>20}".format("Seed err (e):" , str(kData.getGain()*kData.getSeederr()))
#        print "{:>15} {:>20}".format("Seed (e):" , str(kData.getGain()*kData.getSeed()))



#    if len(sys.argv) > 2 and sys.argv[2].isdigit():
#        print "{:>15} {:>20}".format("Seed* (e):" , str(int(sys.argv[2])*kData.getSeed()))
#        print "{:>15} {:>20}".format("Seed err* (e):" , str(int(sys.argv[2])*kData.getSeederr()))




raw_input()
