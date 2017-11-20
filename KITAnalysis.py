import sys,os
from data_grabber import dataGrabber
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from gui import Ui_MainWindow
from strip_mean import strip_mean
from pathlib import Path
# assuming that "KITPlot" is one dir above top level
sys.path.insert(0, Path(os.getcwd()).parents[0])
from KITPlot import KITPlot
from KITPlot.KITConfig import KITConfig

class KITAnalysis(Ui_MainWindow):

    def __init__(self, dialog):

        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        # load gloabals and default values
        settings = KITConfig("Settings.cfg")

        self.cfgFolder = settings["Globals", "cfgPath"]

        self.limitDic = settings["DefaultParameters", "Limits"]

        self.setDefValues(settings)

        # tab 1
        self.as_cfg = settings["DefaultCfgs", "SignalAnnealing"]
        self.vs_cfg = settings["DefaultCfgs", "SignalVoltage"]
        self.rint_cfg = settings["DefaultCfgs", "Rint"]
        self.ncol = 0
        self.chkcol = 7
        self.gcol = 5
        self.projectTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # self.resultTable.setColumnWidth(self.checkCol,68)

        self.updateButton.clicked.connect(self.update_tab1)
        self.startButton.clicked.connect(self.sendRequest)
        self.exportButton.clicked.connect(self.export)
        self.addButton.clicked.connect(self.add)
        self.clearButton.clicked.connect(lambda: self.clear(self.projectTable))
        self.saveButton.clicked.connect(self.save)
        self.drawButton.clicked.connect(self.draw)

        self.projectList = []

        # tab 2
        self.startButton_tab2.clicked.connect(self.sm_start)
        self.clearButton_tab2.clicked.connect(lambda: self.clear(self.resultTable_tab2))
        self.updateButton_tab2.clicked.connect(self.update_tab2)
        self.previewButton_tab2.clicked.connect(self.preview)

    def setDefValues(self,settings):
        self.startBox.setText("229000")
        self.endBox.setText("229800")
        self.valueBox.setText("600")
        self.nameBox.setText("KIT_Test_07")
        self.pathBox.setText(settings["DefaultParameters", "OutputPath"])
        self.projectBox.setText("NewProject")
        self.startBox_tab2.setText("34749")
        self.nameBox_tab2.setText("KIT_Test_23")
        self.pathBox_tab2.setText(settings["DefaultParameters", "OutputPath"])

        for column in range(0,self.limitTable.columnCount()):
            self.limitTable.setItem(0,column,QTableWidgetItem("{:0.1e}".format(self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][0])))
            self.limitTable.setItem(1,column,QTableWidgetItem("{:0.1e}".format(self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][1])))


    def sendRequest(self):
        # reset tabel<
        self.resultTable.setRowCount(0)

        # send search request
        if self.nameBox.text() == "":
            name = None
        else:
            name = "Name=" + self.nameBox.text()

        runNr = self.startBox.text() + "-" + self.endBox.text()
        searchInput = str(self.paraBox.currentText()) + "=" + self.valueBox.text()
        d = dataGrabber()
        self.statusbar.showMessage("Establishing database connection...")
        try:
            self.searchResult = d.main(runNr,searchInput,name)
            if self.searchResult == []:
                self.statusbar.showMessage("Couldn't find data that met the requirements...")
            else:
                self.write_to_table(self.searchResult, self.resultTable)
                self.statusbar.showMessage("Search completed...")
        except:
            self.statusbar.showMessage("Connection failed...")


    def write_to_table(self, result, tab):
        if result == []:
            pass
        else:
            # fill table with data
            if tab == self.resultTable:
                for dic in result:
                    rowPosition = tab.rowCount()
                    tab.insertRow(rowPosition)
                    tab.setItem(rowPosition,self.ncol,QTableWidgetItem(dic["Name"]))
                    tab.setItem(rowPosition,1,QTableWidgetItem(dic["Project"]))
                    tab.setItem(rowPosition,2,QTableWidgetItem(dic["ID"]))
                    tab.setItem(rowPosition,3,QTableWidgetItem(dic["Voltage"]))
                    tab.setItem(rowPosition,4,QTableWidgetItem(dic["Annealing"]))
                    tab.setItem(rowPosition,5,QTableWidgetItem(dic["Gain"]))
                    tab.setItem(rowPosition,6,QTableWidgetItem(dic["Seed"]))

                    # add checkboxes
                    chkBoxItem = QTableWidgetItem()
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Checked)
                    tab.setItem(rowPosition,self.chkcol,chkBoxItem)

            elif tab == self.resultTable_tab2:
                if result[0].getFluenceP() == None:
                    fluence = 0
                else:
                    fluence = result[0].getFluenceP()
                rowPosition = tab.rowCount()
                tab.insertRow(rowPosition)
                tab.setItem(rowPosition,0,QTableWidgetItem(result[0].getName()))
                tab.setItem(rowPosition,1,QTableWidgetItem(result[0].getProject()))
                tab.setItem(rowPosition,2,QTableWidgetItem(str(result[0].getID())))
                tab.setItem(rowPosition,3,QTableWidgetItem(str(fluence)))
                tab.setItem(rowPosition,4,QTableWidgetItem(result[0].getParaY()))
                tab.setItem(rowPosition,5,QTableWidgetItem(result[1][1]))
                tab.setItem(rowPosition,6,QTableWidgetItem(result[1][2]))
                tab.setItem(rowPosition,7,QTableWidgetItem(str(len(result[0].getY())-result[1][0])))

                # add checkboxes
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Checked)
                tab.setItem(rowPosition,8,chkBoxItem)


    def add(self):
        itemList = []
        for i in range(self.resultTable.rowCount()):
            if self.resultTable.item(i, self.chkcol).checkState() == QtCore.Qt.Checked:
                itemList.append(i)

        try:
            newItem = [item for i, item in enumerate(self.searchResult) if i in itemList]

            if newItem in self.projectList:
                # print("Item has already been added to project...")
                self.statusbar.showMessage("Item has already been added to project...")
            else:
                self.projectList.append(newItem)

                # add to project table
                rowPosition = self.projectTable.rowCount()
                self.projectTable.insertRow(rowPosition)
                self.projectTable.setItem(rowPosition,self.ncol,\
                                          QTableWidgetItem(self.projectList[-1][0]["Name"] \
                                          +" ("+self.projectList[-1][0]["Project"]+")"))
        except:
            self.statusbar.showMessage("There is nothing to add...")
            # print("There is nothing to add...")

        return True

    def clear(self, tab):
        if tab == self.projectTable:
            self.projectList = []
            tab.setRowCount(0)
        else:
            tab.setRowCount(0)

    def update_tab1(self):
        for i in range(0,self.resultTable.rowCount()):
            ADC = int(self.searchResult[i]["Seed"])/int(self.searchResult[i]["Gain"])
            self.searchResult[i]["Gain"] = self.resultTable.item(i,self.gcol).text()
            newSeed = round(int(self.searchResult[i]["Gain"])*ADC)
            self.searchResult[i]["Seed"] = str(newSeed)

        self.resultTable.setRowCount(0)
        self.write_to_table(self.searchResult,self.resultTable)
        self.statusbar.showMessage("Table updated...")
        return True

    def update_tab2(self):
        # get new limit values from limitTable and write them into limitDic
        for column in range(0,self.limitTable.columnCount()):
            for row in range(0,2):
                if float(self.limitTable.item(row,column).text()) != self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][row]:
                    self.limitDic[self.limitTable.horizontalHeaderItem(column).text()][row] = float(self.limitTable.item(row,column).text())
        self.clear(self.resultTable_tab2)
        self.sm_start()
        return True

    def save(self):
        newPath = os.path.join(self.pathBox.text(),self.projectBox.text() + "\\")
        if os.path.exists(newPath) == True:
            self.statusbar.showMessage("Path already exists. Rename your old project folder...")
            # print("Path already exists. Rename your old project folder first.")
        else:
            os.mkdir(newPath)
            for item in self.projectList:
                dataGrabber().exportFile(item,self.paraBox.currentText(),newPath)
            self.statusbar.showMessage("Project saved...")
            # print("Project saved...")

        return True

    def sm_start(self):
        data = strip_mean(self.startBox_tab2.text(), self.limitDic).init()
        if isinstance(data, list):
            pass
        else:
            self.write_to_table(data, self.resultTable_tab2)
            self.preview_tab2 = data[0]


    def export(self):
        # send save request
        dataGrabber().exportFile(self.searchResult,self.paraBox.currentText(),self.pathBox.text())

        return True

    def preview(self):
        x = self.preview_tab2.getX()
        y = self.preview_tab2.getY()
        kPlot = KITPlot([x,y],defaultCfg=self.rint_cfg,name="preview")
        kPlot.draw("matplotlib")
        kPlot.saveCanvas()
        kPlot.showCanvas()

    def draw(self):
        projectData = []
        for item in self.projectList:
            x = []
            y = []
            for dic in item:
                x.append(int(dic["Annealing"]))
                y.append(int(dic["Seed"]))
            projectData.append((x,y))

        # if self.projectBox.text() in os.listdir(self.cfgFolder):
        #     os.remove(os.path.join(self.cfgFolder,(self.projectBox.text()+".cfg")))
        # else:
        #     pass
        try:
            if self.paraBox.currentText() == "Voltage":
                kPlot = KITPlot(projectData,
                                defaultCfg=self.as_cfg,
                                name=self.projectBox.text())
            else:
                kPlot = KITPlot(projectData,
                                defaultCfg=self.vs_cfg,
                                name=self.projectBox.text())
            kPlot.draw("matplotlib")
            kPlot.saveCanvas()
            kPlot.showCanvas()
        except(KeyError):
            self.statusbar.showMessage("...")
        except:
            self.statusbar.showMessage("...")


        return True


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # print(QtWidgets.QStyleFactory.keys())
    QtWidgets.QApplication.setStyle("Fusion")
    dialog = QtWidgets.QMainWindow()

    prog = KITAnalysis(dialog)

    dialog.show()
    sys.exit(app.exec_())
