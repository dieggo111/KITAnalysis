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

    def sendInput(self):

        runNr = self.startBox.text() + "-" + self.endBox.text()
        searchInput = str(self.paraBox.currentText()) + "=" + self.valueBox.text()
        d = dataGrabber()
        self.write_to_table(d.main(runNr,searchInput))

    def write_to_table(self, searchList):
        print(searchList)
        for entry in searchList:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

            self.tableWidget.setItem(rowPosition,0,QTableWidgetItem(str(entry[0])))
            self.tableWidget.setItem(rowPosition,1,QTableWidgetItem(str(entry[1])))
            self.tableWidget.setItem(rowPosition,2,QTableWidgetItem(str(entry[2])))
            self.tableWidget.setItem(rowPosition,3,QTableWidgetItem(str(entry[4])))
            self.tableWidget.setItem(rowPosition,4,QTableWidgetItem(str(entry[3])))
            self.tableWidget.setItem(rowPosition,5,QTableWidgetItem(str(entry[5])))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(dialog)

    dialog.show()
    sys.exit(app.exec_())
