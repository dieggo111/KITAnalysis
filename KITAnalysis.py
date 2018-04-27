# pylint: disable=R1710, C0413, C0111, E0602, I1101, C0103, R0913
import sys
import os
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from data_grabber import DataGrabber
from gui import Ui_MainWindow
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, Path(os.getcwd()).parents[0])
from KITPlot import KITPlot
from Resources.InitGlobals import InitGlobals

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
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.initGlobals()
        self.setDefValues()

        # tab1
        add_header(self.resultTab_tab1, len(self.tab1.keys())-1, self.tab1)
        adjust_header(self.projectTable, 1, "Stretch")

        self.updateButton.clicked.connect(self.update_tab1)
        self.startButton.clicked.connect(lambda: self.start_search(self.resultTab_tab1))
        self.exportButton.clicked.connect(lambda: self.exportTable(self.resultTab_tab1))
        self.addButton.clicked.connect(self.add_tab1)
        self.clearButton.clicked.connect(lambda: self.clear(self.projectTable))
        self.saveButton.clicked.connect(self.save_tab1)
        self.drawButton.clicked.connect(self.draw)
        self.projectList = []
        self.seed_adc = {}

        # tab 2
        add_header(self.resultTab_tab2, len(self.tab2.keys())-1, self.tab2)

        self.startButton_tab2.clicked.connect(lambda: self.start_search(self.resultTab_tab2))
        self.clearButton_tab2.clicked.connect(lambda: self.clear(self.resultTab_tab2))
        self.updateButton_tab2.clicked.connect(self.update_tab2)
        self.exportButton_tab2.clicked.connect(lambda: self.exportTable(self.resultTab_tab2))
        self.searchResult_tab2 = []
        self.buttons = []

    def setDefValues(self):
        """ Set limit table values and default values of some boxes which is
        mainly used for debbuging.
        """
        self.valueBox_tab1.setText("600")
        self.nameBox_tab1.setText("KIT_Test_07")
        self.pathBox_tab1.setText(self.outputPath)
        self.projectBox_tab1.setText("NewProject")
        # self.nameBox_tab2.setText("No_Pstop_06")
        self.nameBox_tab2.setText("No_Pstop_06")
        self.projectCombo_tab2.setCurrentIndex(self.projectCombo_tab2.findText(\
            "HPK_2S_II", QtCore.Qt.MatchFixedString))
        self.paraCombo_tab2.setCurrentIndex(self.paraCombo_tab2.findText(\
            "R_int_Ramp", QtCore.Qt.MatchFixedString))
        self.pathBox_tab2.setText(self.outputPath)

        for column in range(0, self.limitTable.columnCount()):
            self.limitTable.setItem(0, column, QTableWidgetItem("{:0.1e}".format(\
                self.limit_dic[self.limitTable.horizontalHeaderItem(column).text()][0])))
            self.limitTable.setItem(1, column, QTableWidgetItem("{:0.1e}".format(\
                self.limit_dic[self.limitTable.horizontalHeaderItem(column).text()][1])))

    def start_search(self, tab):
        """Starts to search data from DB. Executed when the start button is hit.
        Data are then sorted by DataGrabber class and visualized by writing them
        into GUI table.
        """
        self.clear(tab)
        try:
            grabber = DataGrabber(self.db_config)
            if tab == self.resultTab_tab1:
                data_lst = grabber.alibava_search(self.nameBox_tab1.text(),
                                                  self.projectCombo_tab1.currentText(),
                                                  self.paraCombo_tab1.currentText(),
                                                  self.valueBox_tab1.text())
            if tab == self.resultTab_tab2:
                data_lst = grabber.strip_search(self.nameBox_tab2.text(),
                                                self.projectCombo_tab2.currentText(),
                                                self.paraCombo_tab2.currentText(),
                                                self.limit_dic)
            if data_lst == {}:
                raise ValueError
            for dic in data_lst:
                self.write_to_table(dic, tab)
            self.statusbar.showMessage("Search completed...")
        except ValueError:
            self.statusbar.showMessage("Couldn't find data that met the requirements...")

    def write_to_table(self, data_dict, tab):
        """ Fill table with data.
        """
        dic = convert_dict(data_dict)
        row_position = tab.rowCount()
        tab.insertRow(row_position)

        if tab == self.resultTab_tab1:
            ass_dict = self.tab1
            name = self.nameBox_tab1.text()
            project = self.projectCombo_tab1.currentText()
            add_checkbox(tab, row_position, self.tab1["obj"])
            self.resultTab_tab1.setColumnWidth(self.tab1["obj"], 47)
        if tab == self.resultTab_tab2:
            ass_dict = self.tab2
            name = self.nameBox_tab2.text()
            project = self.projectCombo_tab2.currentText()
            add_button(self.resultTab_tab2, self.buttons,
                        row_position, self.tab2["obj"],
                        "Preview", self.preview, data_dict)

        for col in ass_dict:
            if col == "name":
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


    def clear(self, tab):
        if tab == self.projectTable:
            self.projectList = []
        elif tab == self.resultTab_tab2:
            self.buttons = []
        tab.setRowCount(0)

    def update_tab1(self):
        for i in range(0, self.resultTab_tab1.rowCount()):
            new_gain = int(self.resultTab_tab1.item(i, self.tab1["gain"]).text())
            run = int(self.resultTab_tab1.item(i, self.tab1["run"]).text())
            new_seed = str(round(self.seed_adc[run]*new_gain))
            self.resultTab_tab1.setItem(i, self.tab1["seed"],
                                        QTableWidgetItem(new_seed))
        self.statusbar.showMessage("Table updated...")
        return True

    def update_tab2(self):
        # get new limit values from limitTable and write them into limit_dic
        for column in range(0, self.limitTable.columnCount()):
            for row in range(0, 2):
                if float(self.limitTable.item(row, column).text()) \
                        != self.limit_dic[self.limitTable.\
                        horizontalHeaderItem(column).text()][row]:
                    self.limit_dic[self.limitTable.\
                    horizontalHeaderItem(column).text()][row] \
                    = float(self.limitTable.item(row, column).text())
        self.clear(self.resultTab_tab2)
        self.start_search(self.resultTab_tab2)
        return True

    def exportTable(self, tab):
        """Exports content of GUI table to .txt file
        """
        x = []
        if tab == self.resultTab_tab1:
            y = tab.columnCount()-2
            for row in range(0, tab.rowCount()):
                for col in range(0, tab.columnCount()-1):
                    x.append(tab.item(row, col).text())
            if x == []:
                self.statusbar.showMessage("There is nothing to export...")
            else:
                self.write(x, y, path=self.pathBox_tab1.text(),
                           name=self.projectBox_tab1.text())

        elif tab == self.resultTab_tab2:
            y = tab.columnCount()-3
            for row in range(0, tab.rowCount()):
                for col in range(0, tab.columnCount()-2):
                    x.append(tab.item(row, col).text())
            if x == []:
                self.statusbar.showMessage("There is nothing to export...")
            else:
                self.write(x, y,
                           path=self.pathBox_tab2.text(),
                           name=self.nameBox_tab2.text())

    def preview(self, dic):
        """Draws data preview.
        """
        try:
            x = dic["strip"]
            y = dic["data"]
        except KeyError:
            x = [x for x in range(0, len(dic["data"]))]
            y = dic["data"]
        kPlot = KITPlot([(x, y)],
                        defaultCfg=os.path.join("Resources", self.defaultCfgDic\
                                   [dic["para"].replace("_Ramp", "")]),
                        name=dic["para"].replace("_Ramp", ""))
        kPlot.draw("matplotlib")
        # kPlot.saveCanvas()
        kPlot.showCanvas()


    def add_tab1(self):
        itemList = is_checked(self.resultTab_tab1, self.tab1["obj"])
        seed = []
        para = []
        try:
            for row in range(0, self.resultTab_tab1.rowCount()):
                if row in itemList:
                    seed.append(float(self.resultTab_tab1.item(row, self.tab1["seed"]).text()))
                    if self.paraCombo_tab1.currentText() == "Voltage":
                        para.append(float(self.resultTab_tab1.item(row, \
                        self.tab1["annealing"]).text()))
                    elif self.paraCombo_tab1.currentText() == "Annealing":
                        para.append(float(self.resultTab_tab1.item(row, \
                        self.tab1["voltage"]).text()))

            if [para, seed] in self.projectList:
                self.statusbar.showMessage("Item has already been added to project...")
            else:
                self.projectList.append([para, seed])

                # add to project table
                row_position = self.projectTable.rowCount()
                self.projectTable.insertRow(row_position)
                name = self.resultTab_tab1.item(0, self.tab1["name"]).text()\
                       + " ("\
                       + self.resultTab_tab1.item(0, self.tab1["project"]).text()\
                       + ")"
                self.projectTable.setItem(row_position, 0, QTableWidgetItem(name))
        except AttributeError:
            self.clear(self.projectTable)
            self.statusbar.showMessage("There is nothing to add...")

    def save_tab1(self):
        new_path = os.path.join(self.pathBox_tab1.text(),
                               self.projectBox_tab1.text())
        if os.path.exists(new_path) == False:
            os.mkdir(new_path)
        for i, graph in enumerate(self.projectList):
            self.write(graph[0], graph[1], path=new_path,
                       name=self.projectTable.item(i, 0).text())
        self.statusbar.showMessage("Project saved...")
        return True

    # def draw_thread(self):
    #     t = threading.Thread(target=self.draw)
    #     t.run()
    #     # try:
    #         # t.run()
    #     # except:
    #     #     pass
    #     return True

    def draw(self):
        """ projectList contains lists for each graph to be drawn looking like
            [voltage,annealing,seed]
        """
        # check if there's already a cfg file with the same name (this is
        # causing a lot of problems because of the entryList in cfg file)
        cfgName = self.projectBox_tab1.text() + ".cfg"
        i = 1
        while True:
            if cfgName in os.listdir(os.path.join("cfg")):
                cfgName = cfgName.replace(".cfg", str(i) + ".cfg")
                i += 1
            else:
                break

        if self.paraCombo_tab1.currentText() == "Voltage":
            kPlot = KITPlot(self.projectList,
                            defaultCfg=self.defaultCfgDic["SignalVoltage"],
                            name=cfgName)
        elif self.paraCombo_tab1.currentText() == "Annealing":
            kPlot = KITPlot(self.projectList,
                            defaultCfg=self.defaultCfgDic["SignalAnnealing"],
                            name=cfgName)
        kPlot.draw("matplotlib")
        kPlot.showCanvas(save=True)
        return True

    def write(self, x, y, z=None, path=None, name=None):
        if path is None or path == "":
            path = os.getcwd()
        if name is None or name == "":
            name = "NewProject"

        if not os.path.exists(path):
            raise ValueError("Given path does not exist.")
        with open(path + name + ".txt", 'w') as File:
            # export full table
            if isinstance(y, int) and z is None:
                for i, el in enumerate(x):
                    if (i+1)%(y+1) == 0 and i>0:
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
            print("Data written into %s" %(path+name+".txt"))
        return True
###########
#Functions#
###########

def convert_dict(dic):
    """Convert all key and values of a data dict and its nested items into
    strings.
    """
    try:
        return {str(abs(round(key))): convert_value(val) for key, val in dic.items()}
    except TypeError:
        return {key: convert_value(val) for key, val in dic.items()}

def convert_list(lst):
    return [convert_value(item) for item in lst]

def convert_value(val):
    if isinstance(val, dict):
        return convert_dict(val)
    elif isinstance(val, list):
        return convert_list(val)
    elif isinstance(val, (int, float)):
        if abs(val) < 1:
            return str(abs(round(val, 2)))
        return str(abs(round(val)))
    else:
        return val

def is_checked(tab, col):
    item_list = []
    for i in range(tab.rowCount()):
        parent = tab.cellWidget(i, col)
        if parent.findChild(QCheckBox).checkState() == QtCore.Qt.Checked:
            item_list.append(i)
    return item_list

def add_checkbox(tab_obj, row_nr, col_nr):
    """Add a checked checkbox in the center of cell of specific row.
    """
    p_widget = QWidget()
    p_checkbox = QCheckBox()
    p_layout = QHBoxLayout(p_widget)
    p_layout.addWidget(p_checkbox)
    p_layout.setAlignment(QtCore.Qt.AlignCenter)
    p_layout.setContentsMargins(0, 0, 0, 0)
    p_checkbox.setCheckState(QtCore.Qt.Checked)
    add_col(tab_obj, col_nr)
    tab_obj.setCellWidget(row_nr, col_nr, p_widget)
    adjust_header(tab_obj, col_nr, "Stretch")

def add_col(tab_obj, col_nr):
    """Adds a column to TableWidget object.
    """
    tab_obj.setColumnCount(col_nr+1)
    item = QtWidgets.QTableWidgetItem()
    tab_obj.setHorizontalHeaderItem(col_nr, item)

def add_button(tab_obj, button_lst, row_nr, col_nr, name, fun, *args):
    """Add a button at specific position to table.
    """
    button_lst.append(QPushButton(tab_obj))
    button_lst[row_nr].setText(name)
    add_col(tab_obj, col_nr)
    adjust_header(tab_obj, col_nr, "Stretch")
    tab_obj.setCellWidget(row_nr, col_nr, button_lst[row_nr])
    button_lst[row_nr].clicked.connect(lambda: fun(*args))

def adjust_header(tab_obj, count, option="ResizeToContents"):
    """Adjusts header width to column content and table width.

    Args:
        - tab_obj (TableWidget) : table object
        - count (int) : number of columns
        - option (str) : viable attr of QHeaderView. 'Stretch' results in equal
                         column width. 'ResizeToContents' adjusts the column
                         width to content.
    """
    header = tab_obj.horizontalHeader()
    for col in range(0, count):
        header.setSectionResizeMode(col, getattr(QtWidgets.QHeaderView, option))

def add_header(tab_obj, count, info_dict):
    """Adds header objects to TableWidget.
    """
    tab_obj.setColumnCount(count)
    for col in range(0, count):
        item = QtWidgets.QTableWidgetItem()
        item.setText(list(info_dict.keys())[col])
        tab_obj.setHorizontalHeaderItem(col, item)
    adjust_header(tab_obj, count, "Stretch")
    return True

if __name__ == '__main__':

    APP = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle("Fusion")
    DIALOG = QtWidgets.QMainWindow()

    PROG = KITAnalysis(DIALOG)

    DIALOG.show()
    sys.exit(APP.exec_())
