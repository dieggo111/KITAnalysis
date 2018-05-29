"""Globals for KITAnalysis"""
#pylint: disable=R0903, R0902, C0103
# import sys
import os
# from pathlib import Path
# sys.path.insert(0, Path(os.getcwd()).parents[0])
# sys.path.insert(0, Path(os.getcwd()).parents[1])
# print(sys.path)
from KITPlot.KITConfig import KITConfig

class InitGlobals(object):
    """Class containing several variables providing important values for
    KITAnalysis gui"""
    def __init__(self, cwd=os.getcwd()):
        """Initialize global values, create cfg and output folder and Settings
        file if necessary."""
        # create cfg/output folder
        if not os.path.exists(os.path.join(cwd, "cfg")):
            os.mkdir("cfg")
            print("Created cfg folder...")
        if not os.path.exists(os.path.join(cwd, "output")):
            os.mkdir("output")
            print("Created output folder...")
        # and settings file if not existing
        if not os.path.isfile(os.path.join(cwd, "Resources", "Settings.cfg")):
            print("Created settings file...")
            new = KITConfig()
            new.Dir("Resources")
            new.setDict({
                "Globals": {
                    "CredPath"  : ""},
                "DefaultParameters": {
                    "OutputPath": "",
                    "Limits": {
                        "R_int"    : [1e8, 1e13],
                        "R_poly_dc": [1e5, 3e6],
                        "I_leak_dc": [0.01e-9, 1e-9],
                        "Pinhole"  : [0, 8e12],
                        "CC"       : [20e-12, 70e-12],
                        "C_int"    : [0.3e-12, 1.3e-12]}
                },
                "DefaultCfgs": {
                    "SignalVoltage"   : "ALiBaVa_vs_default.cfg",
                    "SignalAnnealing" : "ALiBaVa_as_default.cfg",
                    "R_int"           : "Rint_default.cfg",
                    "C_int"           : "Cint_default.cfg",
                    "R_poly_dc"       : "Rpoly_default.cfg",
                    "Pinhole"         : "Pinhole_default.cfg",
                    "CC"              : "CC_default.cfg",
                    "I_leak_dc"       : "Ileak_default.cfg",
                    "Alpha"           : "Alpha_default.cfg"}})
            new.write("Settings.cfg")

        # load gloabals and default values
        settings = KITConfig(os.path.join("Resources", "Settings.cfg"))
        self.limit_dic = settings["DefaultParameters", "Limits"]
        self.defaultCfgDic = settings["DefaultCfgs"]
        self.outputPath = settings["DefaultParameters", "OutputPath"]

        # load db credentials
        try:
            cnxConf = KITConfig(settings["Globals", "CredPath"])
            self.db_config = cnxConf["database"]
        except:
            raise ValueError("No credentials file found.")

        # accepted projects
        self.projects = ["HPK_2S_I", "HPK_2S_II", "CEC BabyStd", "CEC Bstd",
                         "CEC BPA", "CEC Badd", "CalibrationDiodes"]

        # measurement parameters
        self.strip_paras = ["R_int", "R_int_Ramp", "R_poly_dc", "I_leak_dc",
                            "C_int", "CC", "Pinhole", "C_int_Ramp"]
        self.std_paras = ["C_tot", "I_tot"]


        # set column index dicts
        self.tab1 = {"name"         : 0,
                     "project"      : 1,
                     "run"          : 2,
                     "voltage"      : 3,
                     "annealing"    : 4,
                     "gain"         : 5,
                     "seed"         : 6,
                     "obj"          : 7}

        self.tab2 = {"name"         : 0,
                     "project"      : 1,
                     "pid"          : 2,
                     "voltage"      : 3,
                     "fluence"      : 4,
                     "para"         : 5,
                     "mean"         : 6,
                     "std_err"      : 7,
                     "disc_ratio"   : 8,
                     "obj"          : 9}

        self.tab3 = {"name"         : 0,
                     "project"      : 1,
                     "pid"          : 2,
                     "fluence"      : 3,
                     "annealing"    : 4,
                     "I_0@V"        : 5,
                     "I@V"          : 6,
                     "I_norm@V"     : 7,
                     "obj"          : 8}
