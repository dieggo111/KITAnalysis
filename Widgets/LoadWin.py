# pylint: disable=R1710, C0413, C0111, E0602, I1101, C0103, R0913, W0401, R0902, E0401, W0614, C0301

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from helpers import *


class LoadWin(QWidget):
    querry = QtCore.pyqtSignal(list)
    def __init__(self, tab_obj):
        # super().___init(self)
        QWidget.__init__(self)

        self.setWindowTitle("LoadWin")
        self.setGeometry(QtCore.QRect(400, 400, 700, 200))
        self.tab = tab_obj
        add_header(self.tab, 1, "PID")

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.txt)")[0]
        with open(fname, 'r') as f:
            data = f.read()
            f.close()
        pid_list_str = [pid for pid in data.split("\n") if pid not in ["", " "]]
        pid_list_int = [int(pid) for pid in pid_list_str]
        self.querry.emit(pid_list_int)
        self.fill_table(pid_list_str)

    def fill_table(self, lst):
        for item in lst:
            row = self.tab.rowCount()
            self.tab.insertRow(row)
            tab_item = QTableWidgetItem(item)
            self.tab.setItem(row, 0, tab_item)
