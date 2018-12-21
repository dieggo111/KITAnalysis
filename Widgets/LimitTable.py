# pylint: disable=R1710, C0413, C0111, E0602, I1101, C0103, R0913, W0401, R0902, E0401, W0614, C0301

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from helpers import *



class LimitTable(QWidget):
    querry = QtCore.pyqtSignal(dict)
    def __init__(self, dic):
        # super().___init(self)
        QWidget.__init__(self)
        self.dic = dic

        self.setWindowTitle("Limit Table")
        self.limit_table = QtWidgets.QTableWidget(self)
        self.setGeometry(QtCore.QRect(400, 400, 700, 200))
        self.limit_table.setGeometry(QtCore.QRect(10, 40, 681, 81))
        self.setup_table()
        self.limit_table.itemChanged.connect(self.update_dic)

    def setup_table(self):

        row_names = ["Lower Limit", "Upper Limit"]
        col_names = list(self.dic.keys())
        self.limit_table.setCornerButtonEnabled(True)
        self.limit_table.setStyleSheet("QTableCornerButton::section{border-width: 1px; border-color: #BABABA; border-style:solid;}")

        self.limit_table.setRowCount(len(row_names))
        self.limit_table.setColumnCount(len(self.dic.keys()))
        self.limit_table.setHorizontalHeaderLabels(col_names)

        add_header(self.limit_table, len(row_names),
                   row_names, "vertical")
        add_header(self.limit_table, len(col_names), col_names)

        for i, val in enumerate(self.dic.values()):
            self.limit_table.setItem(0, i,
                                     QTableWidgetItem("{:0.1e}".format(val[0])))
            self.limit_table.setItem(1, i,
                                     QTableWidgetItem("{:0.1e}".format(val[1])))

    def update_dic(self):
        self.dic = read_table(self.limit_table)
        self.send_table()

    def send_table(self):
        self.querry.emit(self.dic)
