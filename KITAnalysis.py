import sys,os
from data_grabber import dataGrabber
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from gui import Ui_MainWindow
from strip_mean import strip_mean
from pathlib import Path
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, Path(os.getcwd()).parents[0])
from KITPlot import KITPlot
from KITPlot.KITConfig import KITConfig
import threading

class KITAnalysis(Ui_MainWindow):

    def __init__(self, dialog):

        # init gui
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        # load gloabals and default values
        settings = KITConfig("Resources\\Settings.cfg")
        self.cfgFolder = settings["Globals", "cfgPath"]
        self.limitDic = settings["DefaultParameters", "Limits"]
        self.defaultCfgDic = settings["DefaultCfgs"]
        self.setDefValues(settings)

        # load db credentials
        try:
            cnxConf = KITConfig(settings["Globals", "credPath"])
            self.db_config = cnxConf["database"]
        except:
            raise ValueError("No credentials file found.")

        # tab 1
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

        self.projectTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.resultTab_tab1.setColumnWidth(self.tab1["check"],68)

        self.updateButton.clicked.connect(self.update_tab1)
        self.startButton.clicked.connect(self.start_tab1)
        self.exportButton.clicked.connect(lambda: self.exportTable(self.resultTab_tab1))
        self.addButton.clicked.connect(self.add_tab1)
        self.clearButton.clicked.connect(lambda: self.clear(self.projectTable))
        self.saveButton.clicked.connect(self.save_tab1)
        self.drawButton.clicked.connect(self.draw_thread)
        self.projectList = []

        # tab 2
        self.startButton_tab2.clicked.connect(self.start_tab2)
        self.clearButton_tab2.clicked.connect(lambda: self.clear(self.resultTab_tab2))
        self.updateButton_tab2.clicked.connect(self.update_tab2)
        self.exportButton_tab2.clicked.connect(lambda: self.exportTable(self.resultTab_tab2))
        self.searchResult_tab2 = []
        self.buttons = []

    def setDefValues(self,settings):
        self.valueBox_tab1.setText("600")
        self.nameBox_tab1.setText("KIT_Test_07")
        self.pathBox_tab1.setText(settings["DefaultParameters", "OutputPath"])
        self.projectBox_tab1.setText("NewProject")
        self.nameBox_tab2.setText("KIT_Test_23")
        self.pathBox_tab2.setText(settings["DefaultParameters", "OutputPath"])

        for column in range(0,self.limitTable.columnCount()):
            self.limitTable.setItem(0,column,QTableWidgetItem("{:0.1e}".format(self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][0])))
            self.limitTable.setItem(1,column,QTableWidgetItem("{:0.1e}".format(self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][1])))

    def start_tab1(self):
        # reset tabel
        self.clear(self.resultTab_tab1)

        # search for data and visualize it
        try:
            grabber = dataGrabber(self.db_config)
            data = grabber.alibava_search(self.nameBox_tab1.text(),
                                          self.projectCombo_tab1.currentText(),
                                          self.paraCombo_tab1.currentText(),
                                          self.valueBox_tab1.text())
            if data == {}:
                raise ValueError
            self.statusbar.showMessage("Search completed...")
            self.write_to_table(data, self.resultTab_tab1)
        except:
            self.statusbar.showMessage("Couldn't find data that met the requirements...")

    def start_tab2(self):
        """
        dataGrabber().strip_search() returns dict[one dict per PID][measurement data and info]
        strip_mean().getMean(dict) returns (dict, (discard ratio, mean val, std error))
        """
        # reset table
        self.clear(self.resultTab_tab2)

        try:
            # get data
            grabber = dataGrabber(self.db_config)
            dic = grabber.strip_search(self.nameBox_tab2.text(),
                                       self.projectCombo_tab2.currentText(),
                                       self.paraCombo_tab2.currentText())
            sm = strip_mean(self.limitDic)
            for sec in dic:
                self.write_to_table(sm.getMean(dic[sec]),self.resultTab_tab2)
            self.statusbar.showMessage("Search completed...")
        except:
            self.statusbar.showMessage("Couldn't find data that met the requirements...")

    def write_to_table(self, result, tab):
        self.seedADC = {}
        if result == {}:
            pass
        else:
            # fill table with data
            if tab == self.resultTab_tab1:
                for sec in result:
                    rowPosition = tab.rowCount()
                    tab.insertRow(rowPosition)
                    tab.setItem(rowPosition,self.tab1["name"],QTableWidgetItem(result[sec]["name"]))
                    tab.setItem(rowPosition,self.tab1["project"],QTableWidgetItem(result[sec]["project"]))
                    tab.setItem(rowPosition,self.tab1["run"],QTableWidgetItem(str(sec)))
                    tab.setItem(rowPosition,self.tab1["voltage"],QTableWidgetItem(result[sec]["voltage"]))
                    tab.setItem(rowPosition,self.tab1["annealing"],QTableWidgetItem(result[sec]["annealing"]))
                    tab.setItem(rowPosition,self.tab1["gain"],QTableWidgetItem(result[sec]["gain"]))
                    tab.setItem(rowPosition,self.tab1["seed"],QTableWidgetItem(result[sec]["seed"]))
                    self.seedADC.update({sec : round(float(result[sec]["seed"])/float(result[sec]["gain"]))})

                    # add checkboxes
                    chkBoxItem = QTableWidgetItem()
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Checked)
                    tab.setItem(rowPosition,self.tab1["check"],chkBoxItem)

            elif tab == self.resultTab_tab2:
                # if result[0].getFluenceP() == None:
                #     fluence = 0
                # else:
                #     fluence = result[0].getFluenceP()
                rowPosition = tab.rowCount()
                tab.insertRow(rowPosition)
                tab.setItem(rowPosition,self.tab2["name"],QTableWidgetItem(result[0]["name"]))
                tab.setItem(rowPosition,self.tab2["project"],QTableWidgetItem(result[0]["project"]))
                tab.setItem(rowPosition,self.tab2["pid"],QTableWidgetItem(str(result[0]["PID"])))
                tab.setItem(rowPosition,self.tab2["fluence"],QTableWidgetItem(result[0]["fluence"] + " " + result[0]["particletype"]))
                tab.setItem(rowPosition,self.tab2["para"],QTableWidgetItem(result[0]["paraY"]))
                tab.setItem(rowPosition,self.tab2["mean"],QTableWidgetItem(result[1][1]))
                tab.setItem(rowPosition,self.tab2["std"],QTableWidgetItem(result[1][2]))
                tab.setItem(rowPosition,self.tab2["discard"],QTableWidgetItem(result[1][0]))

                # add buttons
                self.buttons.append(QPushButton(self.resultTab_tab2))
                self.buttons[rowPosition].setText("Preview")
                tab.setCellWidget(rowPosition,self.tab2["preview"],self.buttons[rowPosition])
                self.buttons[rowPosition].clicked.connect(lambda: self.preview(rowPosition,result[0]))


    def clear(self, tab):
        if tab == self.projectTable:
            self.projectList = []
            tab.setRowCount(0)
        elif tab == self.resultTab_tab2:
            tab.setRowCount(0)
            self.buttons = []
        elif tab == self.resultTab_tab1:
            tab.setRowCount(0)

    def update_tab1(self):
        for i in range(0,self.resultTab_tab1.rowCount()):
            new_gain = int(self.resultTab_tab1.item(i,self.tab1["gain"]).text())
            run = int(self.resultTab_tab1.item(i,self.tab1["run"]).text())
            new_seed = str(self.seedADC[run]*new_gain)
            self.resultTab_tab1.setItem(i,self.tab1["seed"],QTableWidgetItem(new_seed))
        self.statusbar.showMessage("Table updated...")
        return True

    def update_tab2(self):
        # get new limit values from limitTable and write them into limitDic
        for column in range(0,self.limitTable.columnCount()):
            for row in range(0,2):
                if float(self.limitTable.item(row,column).text()) != self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][row]:
                    self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][row] = float(self.limitTable.item(row,column).text())
        self.clear(self.resultTab_tab2)
        self.start_tab2()
        return True

    def exportTable(self,tab):
        x = []
        if tab == self.resultTab_tab1:
            y = tab.columnCount()-2
            for row in range(0,tab.rowCount()):
                for col in range(0,tab.columnCount()-1):
                    x.append(tab.item(row,col).text())
            if x = []:
                self.statusbar.showMessage("There is nothing to export...")
            else:
                self.write(x,y,path=self.pathBox_tab1.text(),name=self.projectBox_tab1.text())

        elif tab == self.resultTab_tab2:
            y = tab.columnCount()-3
            for row in range(0,tab.rowCount()):
                for col in range(0,tab.columnCount()-2):
                    x.append(tab.item(row,col).text())
            if x = []:
                self.statusbar.showMessage("There is nothing to export...")
            else:
                self.write(x,y,path=self.pathBox_tab2.text(),name=self.nameBox_tab2.text())

        return True

    def isChecked(self,tab,col):
        itemList = []
        for i in range(tab.rowCount()):
            if tab.item(i, col).checkState() == QtCore.Qt.Checked:
                itemList.append(i)
        return itemList

    def preview(self,i,dic):

        x = dic["dataX"]
        y = dic["dataY"]
        data = [(x,y)]
        kPlot = KITPlot(data,defaultCfg=self.defaultCfgDic[dic["paraY"]],name=dic["paraY"])
        kPlot.draw("matplotlib")
        kPlot.saveCanvas()
        kPlot.showCanvas()


    def add_tab1(self):
        itemList = self.isChecked(self.resultTab_tab1,self.tab1["check"])
        seed = []
        para = []
        try:
            for row in range(0,self.resultTab_tab1.rowCount()):
                if row in itemList:
                    seed.append(float(self.resultTab_tab1.item(row,self.tab1["seed"]).text()))
                    if self.paraCombo_tab1.currentText() == "Voltage":
                        para.append(float(self.resultTab_tab1.item(row,self.tab1["annealing"]).text()))
                    elif self.paraCombo_tab1.currentText() == "Annealing":
                        para.append(float(self.resultTab_tab1.item(row,self.tab1["voltage"]).text()))

            if [para,seed] in self.projectList:
                self.statusbar.showMessage("Item has already been added to project...")
            else:
                self.projectList.append([para,seed])

                # add to project table
                rowPosition = self.projectTable.rowCount()
                self.projectTable.insertRow(rowPosition)
                self.projectTable.setItem(rowPosition,0,
                                          QTableWidgetItem(self.resultTab_tab1.item(0,self.tab1["name"]).text()
                                          + " ("
                                          + self.resultTab_tab1.item(0,self.tab1["project"]).text()
                                          + ")"))
        except:
            self.statusbar.showMessage("There is nothing to add...")
        return True

    def save_tab1(self):
        newPath = os.path.join(self.pathBox_tab1.text(),self.projectBox_tab1.text() + "\\")
        if os.path.exists(newPath) == False:
            os.mkdir(newPath)
        for i,graph in enumerate(self.projectList):
            self.write(graph[0],graph[1],path=newPath,name=self.projectTable.item(i,0).text())
        self.statusbar.showMessage("Project saved...")
        return True

    def draw_thread(self):
        t = threading.Thread(target=self.draw)
        t.run()
        try:
            t.join()
        except(RuntimeError):
            pass
        return True

    def draw(self):
        """ projectList contains lists for each graph to be drawn looking like
            [voltage,annealing,seed]
        """
        if self.paraCombo_tab1.currentText() == "Voltage":
            kPlot = KITPlot(self.projectList,
                            defaultCfg=self.defaultCfgDic["SignalVoltage"],
                            name=self.projectBox_tab1.text())
        elif self.paraCombo_tab1.currentText() == "Annealing":
            kPlot = KITPlot(self.projectList,
                            defaultCfg=self.defaultCfgDic["SignalAnnealing"],
                            name=self.projectBox_tab1.text())
        try:
            kPlot.draw("matplotlib")
            kPlot.saveCanvas()
            kPlot.showCanvas()
        except(KeyError):
            self.statusbar.showMessage("An error occured while reading cfg. Delete old file or reset EntryList...")
        except:
            self.statusbar.showMessage("An error occured while plotting...")
        return True

    def write(self,x,y,z=None,path=None,name=None):
        if path == None or path == "":
            path = os.getcwd()
        if name == None or name == "":
            name = "NewProject"

        if not os.path.exists(path):
            raise ValueError("Given path does not exist.")
        with open(path + name + ".txt", 'w') as File:
            # export full table
            if isinstance(y, int) and z == None:
                for i, el in enumerate(x):
                    if (i+1)%(y+1) == 0 and i>0:
                        File.write("{:<15}".format(el) + "\n")
                    else:
                        File.write("{:<15}".format(el))
            # export 2 parameters
            elif z == None and all(isinstance(i, list) for i in [x,y]):
                for i,j in list(zip(x,y)):
                    File.write("{:<15} {:<15}".format(i,j) + "\n")
            # export 3 parameters
            elif all(isinstance(i, list) for i in [x,y,z]):
                for i,j,k in list(zip(x,y,z)):
                    File.write("{:<15} {:<15} {:<15}".format(i,j,k) + "\n")
            else:
                self.statusbar.showMessage("An error occured while saving...")

            File.close()
            print ("Data written into %s" %(path+name+".txt"))
        return True


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle("Fusion")
    dialog = QtWidgets.QMainWindow()

    prog = KITAnalysis(dialog)

    dialog.show()
    sys.exit(app.exec_())
