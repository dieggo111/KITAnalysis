# pylint: disable=R1710, C0413, C0111, E0602, I1101, C0103, R0913, W0401, R0902, E0401, W0614, C0301
import sys
import os
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Resources.InitGlobals import InitGlobals
from gui import Ui_MainWindow
from helpers import *
from Widgets.LoadWin import LoadWin
from Widgets.LimitTable import LimitTable
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, Path(os.getcwd()).parents[0])
from KITPlot import KITPlot

class KITAnalysis(Ui_MainWindow, InitGlobals):
    """Search application for ETP DB.

    Methods:
        - ...
    """
    def __init__(self, dialog):
        """Initializes GUI, creates fg/output folder and settings file if not
        existing, loads globals, defaults and credentials. Links buttons to
        class methods.
        """
        super().__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        InitGlobals.__init__(self)

        # statusbar = Statusbar()
        # self.status = QtCore.QThread()
        # self.statusbar.moveToThread(self.status)

        # tab1
        add_header(self.result_tab_1, len(self.tab1.keys())-1, self.tab1)
        adjust_header(self.project_tab_1, 1, "Stretch")
        set_combo_box(self.project_combo_1, self.projects)
        self.updateButton.clicked.connect(self.update_tab1)
        self.startButton.clicked.connect(lambda: self.start_search(self.result_tab_1))
        self.export_button_1.clicked.connect(lambda: self.export_table(self.result_tab_1))
        self.add_button_1.clicked.connect(self.add_to_project_1)
        self.clear_button_1.clicked.connect(lambda: self.clear(self.project_tab_1, self.pid_tab_2))
        self.save_button_1.clicked.connect(lambda: self.save(\
                os.path.join(self.path_box_1.text(),
                             self.project_box_1.text()),
                self.project_lst_1,
                self.project_tab_1))
        self.draw_button_1.clicked.connect(lambda: self.draw(1))
        self.project_lst_1 = []
        self.seed_adc = {}
        self.name_lst_1 = []

        # tab 2
        add_header(self.result_tab_2, len(self.tab2.keys())-1, self.tab2)
        set_combo_box(self.project_combo_2, self.projects)
        set_combo_box(self.para_combo_2, ["*"] + self.strip_paras)
        self.start_button_2.clicked.connect(\
                lambda: self.start_search(self.result_tab_2))
        self.clearButton_tab2.clicked.connect(\
                lambda: self.clear(self.result_tab_2, self.pid_tab_2))
        self.updateButton_tab2.clicked.connect(self.update_tab2)
        self.export_button_2.clicked.connect(\
                lambda: self.export_table(self.result_tab_2))
        self.searchResult_tab2 = []
        self.buttons = []
        self.pid_list = None

        self.lim_popup = LimitTable(self.limit_dic)
        self.lim_popup.querry.connect(self.set_limit_dic)
        self.limit_button_2.clicked.connect(self.show_lim_popup)

        self.load_popup = LoadWin(self.pid_tab_2)
        self.pid_button_2.clicked.connect(self.show_load_popup)
        self.load_popup.querry.connect(self.set_pid_list)

        # tab 3
        add_header(self.result_tab_3, len(self.tab3.keys())-1, self.tab3)
        adjust_header(self.project_tab_3, 1, "Stretch")
        set_combo_box(self.project_combo_3, self.projects)
        self.save_button_3.clicked.connect(lambda: self.save(\
                os.path.join(self.path_box_3.text(),
                             self.project_box_3.text()),
                self.project_lst_3,
                self.project_tab_3))
        self.add_button_3.clicked.connect(self.add_to_project_3)
        self.clear_button_3.clicked.connect(lambda: self.clear(self.project_tab_3))
        self.draw_button_3.clicked.connect(lambda: self.draw(3))
        self.start_button_3.clicked.connect(\
                lambda: self.start_search(self.result_tab_3))
        self.project_lst_3 = []
        self.name_lst_3 = []

        self.set_def_values()


    def set_def_values(self):
        """ Set limit table values and default values of some boxes which is
        mainly used for debbuging.
        """
        self.valueBox_tab1.setText("600")
        self.name_box_1.setText("FZ290_30_Irradiation")
        self.project_combo_1.setCurrentIndex(self.project_combo_1.findText(\
            "HPK_2S_III", QtCore.Qt.MatchFixedString))
        self.path_box_1.setText(self.outputPath)
        self.project_box_1.setText("NewProject")
        # self.name_box_2.setText("No_Pstop_06")
        self.name_box_2.setText("No_Pstop_01")
        self.project_combo_2.setCurrentIndex(self.project_combo_2.findText(\
            "HPK_2S_I", QtCore.Qt.MatchFixedString))
        self.para_combo_2.setCurrentIndex(self.para_combo_2.findText(\
            "R_int_Ramp", QtCore.Qt.MatchFixedString))
        self.pathBox_tab2.setText(self.outputPath)

        self.voltage_box.setText("600")
        # self.name_box_3.setText("FBK_W%")
        self.name_box_3.setText("FZ290_11_Baby")
        self.path_box_3.setText(self.outputPath)
        self.project_box_3.setText("AlphaPlot")
        self.volume_box.setText("0.16688")
        self.project_combo_3.setCurrentIndex(self.project_combo_3.findText(\
            "HPK_2S_III", QtCore.Qt.MatchFixedString))
        self.tabWidget.setCurrentIndex(2)


    def start_search(self, tab):
        """Executed when the start button is hit. Data are visualized by
        writing them into GUI table.
        """
        self.clear(tab)
        if tab == self.result_tab_1:
            search_paras = [1,
                            self.name_box_1.text(),
                            self.project_combo_1.currentText(),
                            self.para_combo_1.currentText(),
                            self.valueBox_tab1.text()]
        if tab == self.result_tab_2:
            search_paras = [2,
                            self.name_box_2.text(),
                            self.project_combo_2.currentText(),
                            self.para_combo_2.currentText(),
                            self.limit_dic,
                            self.pid_list]
        if tab == self.result_tab_3:
            search_paras = [3,
                            self.name_box_3.text(),
                            self.project_combo_3.currentText(),
                            self.voltage_box.text(),
                            self.volume_box.text()]

        self.statusbar.showMessage("Searching...")

        self.thread = QtCore.QThread(self)
        self.search_data = SearchData(self.db_config, search_paras)
        self.search_data.results.connect(self.recieve_data)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.search_data.run)
        self.search_data.moveToThread(self.thread)
        self.thread.start()


    def recieve_data(self, data_lst, tab):
        if data_lst == {} or data_lst == []:
            self.statusbar.showMessage("Couldn't find data that met the requirements...")
        else:
            self.statusbar.showMessage("Search complete...")
            if tab == 1:
                tab = self.result_tab_1
            if tab == 2:
                tab = self.result_tab_2
            if tab == 3:
                tab = self.result_tab_3
            for dic in data_lst:
                self.write_to_table(dic, tab)


    def write_to_table(self, data_dict, tab):
        """ Fill table with data."""
        dic = convert_dict(data_dict)
        row_position = tab.rowCount()
        tab.insertRow(row_position)

        if tab == self.result_tab_1:
            ass_dict = self.tab1
            name = self.name_box_1.text()
            project = self.project_combo_1.currentText()
            add_checkbox(tab, row_position, self.tab1["obj"])
            self.result_tab_1.setColumnWidth(self.tab1["obj"], 47)
        if tab == self.result_tab_2:
            ass_dict = self.tab2
            name = self.name_box_2.text()
            project = self.project_combo_2.currentText()
            add_button(self.result_tab_2, self.buttons,
                       row_position, self.tab2["obj"],
                       "Preview", self.preview, data_dict)
        if tab == self.result_tab_3:
            ass_dict = self.tab3
            name = self.name_box_3.text()
            project = self.project_combo_3.currentText()
            add_checkbox(tab, row_position, self.tab3["obj"], False)
            self.result_tab_3.setColumnWidth(self.tab3["obj"], 47)

        for col in ass_dict:
            if col == "name" and tab != self.result_tab_3:
                tab.setItem(row_position, ass_dict[col],
                            QTableWidgetItem(name))
            elif col == "project":
                tab.setItem(row_position, ass_dict[col],
                            QTableWidgetItem(project))
            elif col == "seed":
                tab.setItem(row_position, ass_dict["seed"],
                            QTableWidgetItem(str(round(data_dict["seed"]*data_dict["gain"]))))
                self.seed_adc.update({data_dict["run"] : data_dict["seed"]})
            elif col == "obj":
                pass
            else:
                tab.setItem(row_position, ass_dict[col],
                            QTableWidgetItem(dic[col]))

    def clear(self, tab, *args):
        if tab == self.project_tab_1:
            self.project_lst_1 = []
        if tab == self.project_tab_3:
            self.project_lst_3 = []
        elif tab == self.result_tab_2:
            self.buttons = []
        tab.setRowCount(0)
        for arg in args:
            arg.setRowCount(0)

    def update_tab1(self):
        for i in range(0, self.result_tab_1.rowCount()):
            new_gain = int(self.result_tab_1.item(i, self.tab1["gain"]).text())
            run = int(self.result_tab_1.item(i, self.tab1["run"]).text())
            new_seed = str(round(self.seed_adc[run]*new_gain))
            self.result_tab_1.setItem(i, self.tab1["seed"],
                                      QTableWidgetItem(new_seed))
        self.statusbar.showMessage("Table updated...")
        return True

    def update_tab2(self):
        self.clear(self.result_tab_2)
        self.start_search(self.result_tab_2)
        return True

    def export_table(self, tab):
        """Exports content of GUI table to .txt file."""
        x = []
        if tab == self.result_tab_1:
            y = tab.columnCount()-2
            for row in range(0, tab.rowCount()):
                for col in range(0, tab.columnCount()-1):
                    x.append(tab.item(row, col).text())
            if x == []:
                self.statusbar.showMessage("There is nothing to export...")
            else:
                self.write(x, y, path=self.path_box_1.text(),
                           name=self.project_box_1.text())

        elif tab == self.result_tab_2:
            y = tab.columnCount()-3
            for row in range(0, tab.rowCount()):
                for col in range(0, tab.columnCount()-2):
                    x.append(tab.item(row, col).text())
            if x == []:
                self.statusbar.showMessage("There is nothing to export...")
            else:
                self.write(x, y,
                           path=self.pathBox_tab2.text(),
                           name=self.name_box_2.text())

    def preview(self, dic):
        """Draws data preview."""
        try:
            x = dic["strip"]
            y = dic["data"]
        except KeyError:
            x = [x for x in range(0, len(dic["data"]))]
            y = dic["data"]

        kPlot = KITPlot(defaultCfg=os.path.join(self.defaultCfgDic\
                                   [dic["para"].replace("_Ramp", "")]))
        kPlot.addFiles([(x, y)], name=dic["para"].replace("_Ramp", ""))
        kPlot.draw()
        # kPlot.saveCanvas()
        kPlot.showCanvas()

    def add_to_project_3(self):
        """Add data from result table on tab 3 to project table/list in order
        to print data."""
        item_lst = is_checked(self.result_tab_3, self.tab3["obj"])
        for row in range(0, self.result_tab_3.rowCount()):
            if row in item_lst:
                x = []
                y = []
                flu = self.result_tab_3.item(row,
                                             self.tab3["fluence"]).text()
                curr = self.result_tab_3.item(row,
                                              self.tab3["I_norm@V"]).text()
                flu = flu.replace("n", "").replace("p", "").replace("np", "")
                x.append(float(flu))
                y.append(float(curr))
                name = self.result_tab_3.item(row, self.tab3["name"]).text() \
                       + " (" \
                       + self.result_tab_3.item(row, self.tab3["project"]).text() \
                       + ")"

                if {name : [x, y]} not in self.project_lst_3:
                    self.project_lst_3.append({name : [x, y]})

                    row_position = self.project_tab_3.rowCount()
                    self.project_tab_3.insertRow(row_position)
                    self.name_lst_3.append(self.result_tab_3.item(\
                            row, self.tab3["name"]).text())
                    self.project_tab_3.setItem(row_position, 0,
                                               QTableWidgetItem(name))

    def add_to_project_1(self):
        """Add data from result table on tab 1 to project table/list in order
        to print data."""
        item_lst = is_checked(self.result_tab_1, self.tab1["obj"])
        seed = []
        para = []
        try:
            for row in range(0, self.result_tab_1.rowCount()):
                if row in item_lst:
                    seed.append(float(self.result_tab_1.item(row, self.tab1["seed"]).text()))
                    if self.para_combo_1.currentText() == "Voltage":
                        para.append(float(self.result_tab_1.item(row, \
                        self.tab1["annealing"]).text()))
                    elif self.para_combo_1.currentText() == "Annealing":
                        para.append(float(self.result_tab_1.item(row, \
                        self.tab1["voltage"]).text()))
            name = self.result_tab_1.item(0, self.tab1["name"]).text()\
                   + " ("\
                   + self.result_tab_1.item(0, self.tab1["project"]).text()\
                   + ")"

            if {name : [para, seed]} in self.project_lst_1:
                self.statusbar.showMessage("Item has already been added to project...")
            else:
                self.project_lst_1.append({name : [para, seed]})

                # add to project table
                row_position = self.project_tab_1.rowCount()
                self.project_tab_1.insertRow(row_position)
                self.name_lst_1.append(name)
                self.project_tab_1.setItem(row_position, 0, QTableWidgetItem(name))
        except AttributeError:
            self.clear(self.project_tab_1)
            self.statusbar.showMessage("There is nothing to add...")

    def save(self, path, project_lst, tab):
        # new_path = os.path.join(self.pathBox_tab1.text(),
        #                         self.project_box_1.text())
        if os.path.exists(path) is False:
            os.mkdir(path)
        for i, dic in enumerate(project_lst):
            self.write(list(dic.values())[0][0], list(dic.values())[0][1],
                       path=path, name=tab.item(i, 0).text())
        self.statusbar.showMessage("Project saved...")
        return True

    def draw(self, tab_nr):
        """ projectList contains lists for each graph to be drawn looking like
            [voltage, annealing, seed]"""
        # check if there's already a cfg file with the same name (this is
        # causing a lot of problems because of the entryList in cfg file)
        if tab_nr == 1:
            cfgName = self.project_box_1.text() + ".cfg"
        if tab_nr == 3:
            cfgName = self.project_box_3.text() + ".cfg"
        i = 1
        while True:
            if cfgName in os.listdir(os.path.join("cfg")):
                cfgName = cfgName.replace(".cfg", str(i) + ".cfg")
                i += 1
            else:
                break
        try:
            if tab_nr == 1 and self.para_combo_1.currentText() == "Voltage":
                lst = [list(dic.values())[0] for dic in self.project_lst_1]
                kPlot = KITPlot(
                    defaultCfg=self.defaultCfgDic["SignalAnnealing"],
                    auto_labeling=False)
                kPlot.addFiles(lst, name=cfgName, name_lst=self.name_lst_1)
                kPlot.draw()
            if tab_nr == 1 and self.para_combo_1.currentText() == "Annealing":
                lst = [list(dic.values())[0] for dic in self.project_lst_1]
                kPlot = KITPlot(
                    defaultCfg=self.defaultCfgDic["SignalVoltage"],
                    auto_labeling=False)
                kPlot.addFiles(lst, name=cfgName, name_lst=self.name_lst_1)
                kPlot.draw()
            if tab_nr == 3:
                lst = [list(xy_pair.values())[0] for xy_pair in self.project_lst_3]
                kPlot = KITPlot(
                    defaultCfg=self.defaultCfgDic["Alpha"], auto_labeling=False)
                f, t = kPlot.get_fit(lst)
                kPlot.addFiles(lst, name=cfgName, name_lst=self.name_lst_3)
                kPlot.draw()
                fig = kPlot.getCanvas()
                kPlot.addLodger(fig, t, f)

            kPlot.showCanvas(save=True)
        except TypeError:
            self.statusbar.showMessage("There's nothing to draw...")
        return True

    def write(self, x, y, z=None, path=None, name=None):
        if path is None or path == "":
            path = os.getcwd()
        if name is None or name == "":
            name = "NewProject"

        if not os.path.exists(path):
            raise ValueError("Given path does not exist.")
        with open(os.path.join(path, name + ".txt"), 'w') as File:
            # export full table
            if isinstance(y, int) and z is None:
                for i, el in enumerate(x):
                    if (i + 1)%(y + 1) == 0 and i > 0:
                        File.write("{:<15}".format(el) + "\n")
                    else:
                        File.write("{:<15}".format(el))
            # export 2 parameters
            elif z is None and all(isinstance(i, list) for i in [x, y]):
                for i, j in list(zip(x, y)):
                    File.write("{:<15} {:<15}".format(i, j) + "\n")
            # export 3 parameters
            elif all(isinstance(i, list) for i in [x, y, z]):
                for i, j, k in list(zip(x, y, z)):
                    File.write("{:<15} {:<15} {:<15}".format(i, j, k) + "\n")
            else:
                self.statusbar.showMessage("An error occured while saving...")

            File.close()
            print("Data written into %s" %os.path.join(path, name + ".txt"))
        return True

    def set_limit_dic(self, dic):
        self.limit_dic = dic

    # def complete(self):
    #     self.statusbar.showMessage("Search completed...")
        # self.progress_bar.setVisible(False)

    def show_lim_popup(self):
        self.lim_popup.show()

    def show_load_popup(self):
        self.load_popup.getfile()

    def set_pid_list(self, lst):
        self.pid_list = lst





# class Statusbar(QtCore.Object):
#     """Some fancy statusbar job while queuing"""
#     def __init__(self, option="spinner"):
#         super().__init__()
#
#     def load(self):
#         pass
#
#     def show(self, msg):
#         pass

# def statusbar_load(queue, statusbar_obj, option="spinner"):
#
#     data = None
#     i = 0
#     while data is None:
#         try:
#             data = queue.get(timeout=0.1)
#         except Empty:
#             if option == "spinner":
#                 status = ["-", "\\", "|", "/"]
#                 statusbar_obj.showMessage("Searching  [" + status[i%4] + "]")
#             if option == "loader":
#                 status = "|"
#                 space = " "
#                 statusbar_obj.showMessage("Searching   [" + (i%31)*status
#                                           + (30-i%31)*space + "]")
#             i = i + 1
#     return data



if __name__ == '__main__':

    APP = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle("Fusion")
    DIALOG = QtWidgets.QMainWindow()

    PROG = KITAnalysis(DIALOG)

    DIALOG.show()
    sys.exit(APP.exec_())
