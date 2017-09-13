import sys
from data_grabber import dataGrabber
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from search_gui import Ui_MainWindow

class MyFirstGuiProgram(Ui_MainWindow):

    def __init__(self, dialog):

        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.startButton.clicked.connect(self.sendInput)
        self.saveButton.clicked.connect(self.save)
        self.drawButton.clicked.connect(self.draw)
        self.resultTable = []

    def sendInput(self):

        # reset tabel
        self.tableWidget.setRowCount(0)

        # send search request
        if self.nameBox.text() == "":
            name = None
        else:
            name = "Name=" + self.nameBox.text()

        runNr = self.startBox.text() + "-" + self.endBox.text()
        searchInput = str(self.paraBox.currentText()) + "=" + self.valueBox.text()
        d = dataGrabber()
        self.result = d.main(runNr,searchInput,name)
        self.write_to_table(self.result)


    def write_to_table(self, resultList):

        # fill table with data
        for dic in resultList:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition,0,QTableWidgetItem(dic["Name"]))
            self.tableWidget.setItem(rowPosition,1,QTableWidgetItem(dic["ID"]))
            self.tableWidget.setItem(rowPosition,2,QTableWidgetItem(dic["Voltage"]))
            self.tableWidget.setItem(rowPosition,3,QTableWidgetItem(dic["Annealing"]))
            self.tableWidget.setItem(rowPosition,4,QTableWidgetItem(dic["Gain"]))
            self.tableWidget.setItem(rowPosition,5,QTableWidgetItem(dic["Seed"]))

            # add checkboxes
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(rowPosition,6,chkBoxItem)

    def draw(self, item):
        self.list = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 6).checkState() == QtCore.Qt.Checked:
                self.list.append(i)

        print(self.list)

    def save(self):

        # send save request
        d = dataGrabber()
        d.exportFile(self.result,self.paraBox.currentText(),self.pathBox.text())

        return True


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(dialog)

    dialog.show()
    sys.exit(app.exec_())
