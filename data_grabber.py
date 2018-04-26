# pylint: disable=R1710, C0413, C0111
import sys
import os
from pathlib import Path
import numpy as np
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, str(Path(os.getcwd()).parents[0]))
from KITPlot.KITSearch import KITSearch

class DataGrabber(object):
    """Grab data dict and convert/format it according to specifications of app.
    """
    def __init__(self, credentials):
        """Load globals.
        """
        self.__para_lst = ["Voltage", "Annealing"]
        self.__default_gain = 210
        self.__annealing_norm = 1
        self.db_creds = credentials
        self.strip_meas = ["R_int", "R_int_Ramp", "R_poly_dc", "I_leak_dc",
                           "C_int", "CC", "Pinhole", "C_int_Ramp"]
        self.std_meas = ("C_tot", "I_tot")

    def strip_search(self, name, project, para, limit_dic):
        """Format data dict according to table specifications.

        Returns: [{measurment data for v_bais1}, {measurment data for v_bais2},
                 ...]
        """
        session = KITSearch(self.db_creds)
        dic = session.probe_search_for_name(name, project)
        if para == "*":
            dic = pop_items(dic, "IVCV", self.std_meas, self.strip_meas)
            data_lst = handle_asterisk(dic)
        else:
            dic = pop_items(dic, para, self.std_meas, self.strip_meas)
            if "Ramp" in para:
                data_lst = reshuffle_for_ramp(dic, para)
            else:
                data_lst = reshuffle_for_strip(dic)
        data_lst = get_mean(data_lst, limit_dic)
        return data_lst

    def alibava_search(self, name, project, para, value):
        """Format data dict according to table specifications.
        """
        session = KITSearch(self.db_creds)
        if para == "Voltage":
            dic = session.ali_search_for_name_voltage(name, int(value), project)
        elif para == "Annealing":
            dic = session.ali_search_for_name_annealing(name, int(value), project)
        dic = pop_items(dic, "unanalyzed", self.std_meas, self.strip_meas)
        data_lst = reshuffle_for_alibava(dic)
        return data_lst


############
# Functions#
############

def handle_asterisk(data):
    """Handles the shuffeling of a search with undefined parameter.
    """
    data_lst = []
    cint_dict = {}
    rint_dict = {}
    strip_dict = {}
    for sec in data:
        if "C_int_Ramp" in data[sec]["paraY"]:
            cint_dict[sec] = data[sec]
        elif "R_int_Ramp" in data[sec]["paraY"]:
            rint_dict[sec] = data[sec]
        else:
            strip_dict[sec] = data[sec]
    data_lst = reshuffle_for_ramp(rint_dict, "R_int_Ramp")\
               + reshuffle_for_ramp(cint_dict, "C_int_Ramp")\
               + reshuffle_for_strip(strip_dict)
    return data_lst

def get_mean(data, limit_dic):
    """Calculates mean value and std deviation of data.
    """
    for dic in data:
        corr_lst = []
        for val in dic["data"]:
            try:
                if limit_dic[dic["para"]][0] < abs(val) < limit_dic[dic["para"]][1]:
                    corr_lst.append(val)
            except KeyError:
                corr_lst.append(val)
        dic["disc_ratio"] = (len(dic["data"])-len(corr_lst))/len(dic["data"])
        dic["mean"] = "{:0.3e}".format(np.mean(corr_lst))
        dic["std_err"] = "{:0.3e}".format(np.std(corr_lst))
    return data


def pop_items(dic, opt, std_meas, strip_meas):
    """Pop unwanted measurements/runs from data dict.
    """
    del_lst = []
    for sec in dic:
        if opt == "unanalyzed" and dic[sec]["gain"] is None:
            del_lst.append(sec)
        elif opt == "IVCV" and dic[sec]["paraY"] in std_meas:
            del_lst.append(sec)
        elif opt in strip_meas and dic[sec]["paraY"] != opt:
            del_lst.append(sec)
    for run in del_lst:
        dic.pop(run)
    return dic

def reshuffle_for_alibava(data):
    """Reshuffels data dict for ramp measurements in order to meet
    specifications of app regarding alibava measurements.

    Returns: [{measurment data for v_bais1}, {measurment data for v_bais2}, ...]
    """
    data_lst = []
    for sec in data:
        data_lst.append({"voltage" : data[sec]["voltage"],
                         "run" : sec,
                         "annealing" : data[sec]["annealing"],
                         "gain" : data[sec]["gain"],
                         "seed" : data[sec]["seed"],
                         "fluence" : make_flu_par(data[sec]["fluence"], \
                         data[sec]["particletype"])})
    return data_lst

def reshuffle_for_strip(data):
    """Reshuffels data dict for ramp measurements in order to meet
    specifications of app regarding strip measurements.

    Returns: [{measurment data for v_bais1}, {measurment data for v_bais2}, ...]
    """
    data_lst = []
    for sec in data:
        data_lst.append({"voltage" : data[sec]["dataZ"][0],
                         "pid" : data[sec]["PID"],
                         "para" : data[sec]["paraY"],
                         "data" : data[sec]["dataY"],
                         "fluence" : make_flu_par(data[sec]["fluence"], \
                         data[sec]["particletype"]),
                         "strip" : data[sec]["dataX"]})
    return data_lst

def reshuffle_for_ramp(data, para=None):
    """Reshuffels data dict for ramp measurements in order to meet
    specifications of app regarding ramp measurements.

    Returns: [{measurment data for v_bais1}, {measurment data for v_bais2}, ...]
    """
    new_data = []
    ass_dict = {}
    voltage_values = []
    for pid, dic in data.items():
        flu_par = make_flu_par(dic["fluence"], dic["particletype"])
        if flu_par not in ass_dict.keys():
            ass_dict[flu_par] = []
    for key in ass_dict:
        for pid, dic in data.items():
            if flu_par == key:
                ass_dict[key].append(pid)
    for dic in data.values():
        for volt in dic["dataZ"]:
            if volt not in voltage_values:
                voltage_values.append(volt)
    for flu, lst in ass_dict.items():
        v_r_dict = get_ramp_data(lst, voltage_values, data)
        for key, val in v_r_dict.items():
            new_data.append({"voltage" : key, "fluence" : flu,
                             "pid" : "-", "data": val})
    try:
        for dic in new_data:
            dic["para"] = para
    except ValueError:
        pass
    return new_data

def get_ramp_data(ass_lst, volt_lst, data_dict):
    """Loops through assosiation list and voltage list and extracts the measured
    quantities for each voltage ramp step.

    Returns: {v_bais1 : [val1, val2, ...], v_bias2 : [...], ...}
    """
    v_r_dict = {}
    for pid in ass_lst:
        for volt in volt_lst:
            if volt in data_dict[pid]["dataZ"]:
                try:
                    v_r_dict[volt].append(data_dict[pid]["dataY"][\
                            data_dict[pid]["dataZ"].index(volt)])
                except KeyError:
                    v_r_dict[volt] = [data_dict[pid]["dataY"][\
                            data_dict[pid]["dataZ"].index(volt)]]
    return v_r_dict

def make_flu_par(flu, par):
    """Create a string containing fluence and particletype.
    """
    flu_par = "{:.2e}".format(flu) + par
    return flu_par
