import sys,os
from data_grabber import dataGrabber
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from search_gui import Ui_MainWindow
sys.path.append("C:\\Users\\Marius\\KITPlot\\")
from KITPlot import KITPlot

class KITAnalysis(Ui_MainWindow):

    def __init__(self, dialog):

        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.cfgFolder = "C:\\Users\\Marius\\KITPlot\\Analysis_Tools\\cfg\\"
        self.as_cfg = "ALiBaVa_as_default.cfg"
        self.vs_cfg = "ALiBaVa_vs_default.cfg"
        self.nameCol = 0
        self.projectCol = 1
        self.runCol = 2
        self.voltCol = 3
        self.annealCol = 4
        self.gainCol = 5
        self.seedCol = 6
        self.checkCol = 7

        self.projectTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.resultTable.setColumnWidth(self.checkCol,68)

        self.updateButton.clicked.connect(self.update)
        self.startButton.clicked.connect(self.sendRequest)
        self.exportButton.clicked.connect(self.export)
        self.addButton.clicked.connect(self.add)
        self.clearButton.clicked.connect(self.clear)
        self.saveButton.clicked.connect(self.save)
        self.drawButton.clicked.connect(self.draw)

        self.projectList = []

    def sendRequest(self):
        # reset tabel
        self.resultTable.setRowCount(0)

        # send search request
        if self.nameBox.text() == "":
            name = None
        else:
            name = "Name=" + self.nameBox.text()

        runNr = self.startBox.text() + "-" + self.endBox.text()
        searchInput = str(self.paraBox.currentText()) + "=" + self.valueBox.text()
        d = dataGrabber()
        self.searchResult = d.main(runNr,searchInput,name)
        self.write_to_table()



    def write_to_table(self):
        if self.searchResult == []:
            pass
        else:
            # fill table with data
            for dic in self.searchResult:
                rowPosition = self.resultTable.rowCount()
                self.resultTable.insertRow(rowPosition)
                self.resultTable.setItem(rowPosition,self.nameCol,QTableWidgetItem(dic["Name"]))
                self.resultTable.setItem(rowPosition,self.projectCol,QTableWidgetItem(dic["Project"]))
                self.resultTable.setItem(rowPosition,self.runCol,QTableWidgetItem(dic["ID"]))
                self.resultTable.setItem(rowPosition,self.voltCol,QTableWidgetItem(dic["Voltage"]))
                self.resultTable.setItem(rowPosition,self.annealCol,QTableWidgetItem(dic["Annealing"]))
                self.resultTable.setItem(rowPosition,self.gainCol,QTableWidgetItem(dic["Gain"]))
                self.resultTable.setItem(rowPosition,self.seedCol,QTableWidgetItem(dic["Seed"]))

                # add checkboxes
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Checked)
                self.resultTable.setItem(rowPosition,self.checkCol,chkBoxItem)


    def add(self):
        itemList = []
        for i in range(self.resultTable.rowCount()):
            if self.resultTable.item(i, self.checkCol).checkState() == QtCore.Qt.Checked:
                itemList.append(i)

        newItem = [item for i, item in enumerate(self.searchResult) if i in itemList]
        if newItem in self.projectList:
            print("Item has already been added to project...")
        else:
            self.projectList.append(newItem)

            # add to project table
            rowPosition = self.projectTable.rowCount()
            self.projectTable.insertRow(rowPosition)
            self.projectTable.setItem(rowPosition,self.nameCol,\
                                      QTableWidgetItem(self.projectList[-1][0]["Name"] \
                                      +" ("+self.projectList[-1][0]["Project"]+")"))

        return True

    def clear(self):
        # reset tabel
        self.projectTable.setRowCount(0)
        self.projectList = []
        return True

    def update(self):
        for i in range(0,self.resultTable.rowCount()):
            ADC = int(self.searchResult[i]["Seed"])/int(self.searchResult[i]["Gain"])
            self.searchResult[i]["Gain"] = self.resultTable.item(i,self.gainCol).text()
            newSeed = round(int(self.searchResult[i]["Gain"])*ADC)
            self.searchResult[i]["Seed"] = str(newSeed)

        self.resultTable.setRowCount(0)
        self.write_to_table()
        return True

    def save(self):
        newPath = os.path.join(self.pathBox.text(),self.projectBox.text() + "\\")
        if os.path.exists(newPath) == True:
            print("Path already exists. Rename your old project folder first.")
        else:
            os.mkdir(newPath)
            for item in self.projectList:
                dataGrabber().exportFile(item,self.paraBox.currentText(),newPath)
            print("Project saved...")

        return True

    def export(self):
        # send save request
        dataGrabber().exportFile(self.searchResult,self.paraBox.currentText(),self.pathBox.text())

        return True

    def draw(self):
        projectData = []
        for item in self.projectList:
            x = []
            y = []
            for dic in item:
                x.append(int(dic["Annealing"]))
                y.append(int(dic["Seed"]))
            projectData.append((x,y))

        if self.projectBox.text() in os.listdir(self.cfgFolder):
            os.remove(os.path.join(self.cfgFolder,(self.projectBox.text()+".cfg")))
        else:
            pass

        if self.paraBox.currentText() == "Voltage":
            kPlot = KITPlot(projectData,
                            defaultCfg=os.path.join(self.cfgFolder,self.as_cfg),
                            name=self.projectBox.text())
        else:
            kPlot = KITPlot(projectData,
                            defaultCfg=os.path.join(self.cfgFolder,self.vs_cfg),
                            name=self.projectBox.text())
        kPlot.draw("matplotlib")
        kPlot.saveCanvas()
        kPlot.showCanvas()
        return True


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # print(QtWidgets.QStyleFactory.keys())
    QtWidgets.QApplication.setStyle("Fusion")
    dialog = QtWidgets.QMainWindow()

    prog = KITAnalysis(dialog)

    dialog.show()
    sys.exit(app.exec_())
