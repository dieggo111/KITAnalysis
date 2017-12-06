# sys.path.insert(0, Path(os.getcwd()).parents[0])
import sys,os
from KITPlot.KITConfig import KITConfig
# from pathlib import Path

class InitGlobals(object):
    def initGlobals(self,cwd=os.getcwd()):
        # create cfg/output folder
        if not os.path.exists(os.path.join(cwd,"cfg")):
            os.mkdir("cfg")
            print("Created cfg folder...")
        if not os.path.exists(os.path.join(cwd,"output")):
            os.mkdir("output")
            print("Created output folder...")
        # and settings file if not existing
        if not os.path.isfile(os.path.join(cwd,"Resources","Settings.cfg")):
            print("Created settings file...")
            new = KITConfig()
            new.Dir("Resources\\")
            new.setDict({
                            "Globals": {
                                "CredPath"  : ""},
                            "DefaultParameters": {
                                "OutputPath": "",
                                "Limits": {
                                    "R_int"    : [1e8,1e13],
                                    "R_poly_dc": [1e5,3e6],
                                    "I_leak_dc": [0.01e-9,1e-9],
                                    "Pinhole"  : [0,8e12],
                                    "CC"       : [20e-12,70e-12],
                                    "C_int"    : [0.3e-12,1.3e-12]}
                            },
                            "DefaultCfgs": {
                                "SignalVoltage"   : os.path.join("Resources","ALiBaVa_vs_default.cfg"),
                                "SignalAnnealing" : os.path.join("Resources","ALiBaVa_as_default.cfg"),
                                "R_int"           : os.path.join("Resources","Rint_default.cfg"),
                                "C_int"           : os.path.join("Resources","Cint_default.cfg"),
                                "R_poly_dc"       : os.path.join("Resources","Rpoly_default.cfg"),
                                "Pinhole"         : os.path.join("Resources","Pinhole_default.cfg"),
                                "CC"              : os.path.join("Resources","CC_default.cfg"),
                                "I_leak_dc"       : os.path.join("Resources","Ileak_default.cfg")}})
            new.write("Settings.cfg")

        # load gloabals and default values
        settings = KITConfig(os.path.join("Resources","Settings.cfg"))
        self.limitDic = settings["DefaultParameters", "Limits"]
        self.defaultCfgDic = settings["DefaultCfgs"]
        self.outputPath = settings["DefaultParameters", "OutputPath"]

        # load db credentials
        try:
            cnxConf = KITConfig(settings["Globals", "CredPath"])
            self.db_config = cnxConf["database"]
        except:
            raise ValueError("No credentials file found.")

        # set column index dicts
        self.tab1 = {"name"         : 0,
                     "project"      : 1,
                     "run"          : 2,
                     "voltage"      : 3,
                     "annealing"    : 4,
                     "gain"         : 5,
                     "seed"         : 6,
                     "check"        : 7}

        self.tab2 = {"name"         : 0,
                     "project"      : 1,
                     "pid"          : 2,
                     "fluence"      : 3,
                     "para"         : 4,
                     "mean"         : 5,
                     "std"          : 6,
                     "discard"      : 7,
                     "preview"      : 8}
