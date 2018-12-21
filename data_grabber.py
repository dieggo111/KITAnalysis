# pylint: disable=R1710, C0413, C0111, E0401, R0913
import sys
import os
from pathlib import Path
import numpy as np
# from Resources.InitGlobals import InitGlobals
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, str(Path(os.getcwd()).parents[0]))
from KITPlot.KITSearch import KITSearch

STRIP_PARAS = ["R_int", "R_int_Ramp", "R_poly_dc", "I_leak_dc",
               "C_int", "CC", "Pinhole", "C_int_Ramp"]
STD_PARAS = ["C_tot", "I_tot"]

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


    def alpha_search(self, name, project, t_vol, volume):
        """Format data dict according to table specifications."""
        session = KITSearch(self.db_creds)
        dic = session.probe_search(name, project)
        dic = pop_items(dic, "I_tot", STD_PARAS, STRIP_PARAS)
        data_lst = reshuffle_for_alpha(dic, float(t_vol), float(volume))
        return data_lst

    def strip_search(self, name, project, para, limit_dic, pid_list=None):
        """Format data dict according to table specifications.

        Returns: [{measurment data for item1}, {measurment data for item2},
                 ...]
        """
        session = KITSearch(self.db_creds)
        dic = session.probe_search(name, project, pid_list)
        if para == "*":
            dic = pop_items(dic, "IVCV", STD_PARAS, STRIP_PARAS)
            data_lst = handle_asterisk(dic)
        else:
            dic = pop_items(dic, para, STD_PARAS, STRIP_PARAS)
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
        dic = session.ali_search_data(name, project, para, int(value))
        dic = pop_items(dic, "unanalyzed", STD_PARAS, STRIP_PARAS)
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
        if "_Ramp" in dic["para"]:
            para = dic["para"].replace("_Ramp", "")
        else:
            para = dic["para"]
        for val in dic["data"]:
            try:
                if limit_dic[para][0] < abs(val) < limit_dic[para][1]:
                    corr_lst.append(val)
            except KeyError:
                corr_lst.append(val)
        dic["disc_ratio"] = (len(dic["data"])-len(corr_lst))/len(dic["data"])
        dic["mean"] = "{:0.3e}".format(np.mean(corr_lst))
        dic["std_err"] = "{:0.3e}".format(np.std(corr_lst)/np.sqrt(len(corr_lst)))
    return data


def pop_items(dic, opt, std_meas, strip_meas):
    """Pop unwanted measurements/runs from data dict.

    Args:
        - opt (str): a) "unanalyzed" deletes unanalyzed alibava runs and old
                        runs without gain value
                     b) "IVCV" deletes IV and CV measurements
                     c) <strip measurement> deletes all other measurements
                     d) "alpha" deletes measurements without fluence
    """
    del_lst = []
    for sec in dic:
        if opt == "unanalyzed" and dic[sec]["gain"] is None:
            del_lst.append(sec)
        elif opt == "IVCV" and dic[sec]["paraY"] in std_meas:
            del_lst.append(sec)
        elif opt in strip_meas+std_meas and dic[sec]["paraY"] != opt:
            del_lst.append(sec)
        elif opt == "alpha" and dic[sec]["fluence"] == 0:
            del_lst.append(sec)
        elif dic[sec]["flag"] == "bad":
            del_lst.append(sec)
    for run in del_lst:
        dic.pop(run)
    return dic

def reshuffle_for_alpha(data, tar_volt, volume):
    """Reshuffels data dict for alpha plots. Get leakage current at target
    voltage before irradiation if possible. Then get leakage current at target
    voltage after irradiation and normalize data.

    Returns: [{measurment data for v_bais1}, {measurment data for v_bais2}, ...]
    """
    data_lst = []

    curr_0_dict = find_curr_in_dict(data, tar_volt, False)
    curr_dict = find_curr_in_dict(data, tar_volt, True)
    for sec in data:
        if data[sec]["fluence"] != 0:
            data_lst.append({"name" : data[sec]["name"],
                             "voltage" : tar_volt,
                             "I_0@V" : curr_0_dict[data[sec]["name"]][0],
                             "I_norm@V" : norm_curr(\
                                    curr_dict[data[sec]["name"]][0],
                                    volume,
                                    curr_dict[data[sec]["name"]][1],
                                    curr_0_dict[data[sec]["name"]][0]),
                             "I@V" : curr_dict[data[sec]["name"]][0],
                             "pid" : data[sec]["PID"],
                             "para" : data[sec]["paraY"],
                             "annealing" : format_ann(data[sec]["annealing"]),
                             "fluence" : format_flu_par(\
                                    data[sec]["fluence"],
                                    data[sec]["particletype"])})
    return data_lst

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
                         "fluence" : format_flu_par(data[sec]["fluence"], \
                         data[sec]["particletype"])})
    return data_lst

def reshuffle_for_strip(data):
    """Reshuffels data dict for ramp measurements in order to meet
    specifications of app regarding strip measurements.

    Returns: [{measurment data for item1}, {measurment data for item2}, ...]
    """
    data_lst = []
    for sec in data:
        data_lst.append({"voltage" : data[sec]["dataZ"][0],
                         "pid" : data[sec]["PID"],
                         "para" : data[sec]["paraY"],
                         "data" : data[sec]["dataY"],
                         "fluence" : format_flu_par(data[sec]["fluence"], \
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
        flu_par = format_flu_par(dic["fluence"], dic["particletype"])
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

def find_curr_in_dict(data, tar_volt, irr):
    """Find current value at target voltage before irradiation of specific
    sensor"""
    dic = {}
    for sec in data:
        if irr is False:
            if data[sec]["fluence"] == 0 and data[sec]["flag"] == "valid":
                dic[data[sec]["name"]] = find_curr(data[sec]["dataX"],
                                                   data[sec]["dataY"],
                                                   data[sec]["temp"],
                                                   irr,
                                                   tar_volt)
            elif data[sec]["fluence"] == 0 and data[sec]["flag"] == "good" \
                    and data[sec]["name"] not in dic.keys():
                dic[data[sec]["name"]] = find_curr(data[sec]["dataX"],
                                                   data[sec]["dataY"],
                                                   data[sec]["temp"],
                                                   irr,
                                                   tar_volt)
        else:
            if not data[sec]["fluence"] == 0 and data[sec]["flag"] == "valid":
                dic[data[sec]["name"]] = find_curr(data[sec]["dataX"],
                                                   data[sec]["dataY"],
                                                   data[sec]["temp"],
                                                   irr,
                                                   tar_volt)
            elif not data[sec]["fluence"] == 0 and data[sec]["flag"] == "good" \
                    and data[sec]["name"] not in dic.keys():
                dic[data[sec]["name"]] = find_curr(data[sec]["dataX"],
                                                   data[sec]["dataY"],
                                                   data[sec]["temp"],
                                                   irr,
                                                   tar_volt)
    return dic

def find_curr(datax, datay, datat, irr, tar_volt):
    """Zips voltage, current and temperature lists in order to find the current
    at a certain voltage. Also checks if temperature is in the expected range.

    Args:
        - datax (list) : voltage list
        - datay (list) : current list
        - datat (list) : temperature list
        - irr (bool) : default temperature is -20 for irradiated and 20 for
                       unirradiated samples
        - tar_volt (float) : target voltage
    """
    if irr is True:
        temp = -20
    if irr is False:
        temp = 20
    for x_val, y_val, temp_val in zip(datax, datay, datat):
        if (abs(tar_volt)*0.99) < abs(x_val) < (abs(tar_volt)*1.01):
            if irr is True and (temp*1.05) < temp_val < (temp*0.95):
                return (y_val, temp_val)
            if irr is False and (temp*0.95) < temp_val < (temp*1.05):
                return (y_val, temp_val)
    return 0

def format_flu_par(flu, par):
    """Create a string containing fluence and particletype.
    """
    if set(par) == set(["n", "p"]):
        par = "np"
    elif len(par) == 1:
        par = par[0]
    else:
        par = ""
    flu_par = "{:.2e}".format(flu) + par
    return flu_par

def format_ann(ann, scale="days"):
    """Create a string containing annealing time in hours or weeks with
    attached unit symbol.
    """
    if scale == "days":
        return str(round(ann/24)) + "d (" + str(round(ann)) + "h)"
    if scale == "weeks":
        return str(round(ann/24/7, 1)) + "w (" + str(round(ann)) + "h)"

def norm_curr(curr, volume, temp, curr_0):
    """Normalize current to volume and 20°C."""
    delta = curr/volume - curr_0/volume
    if temp < 19:
        delta = delta*(293/(273+temp))**2*np.exp(-1.21/(2*1.38*10**-23)\
                *1.6*(10**-19)*(1/293-1/(273+temp)))
    return delta
