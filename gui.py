"""GUI of KITAnalysis app"""
# -*- coding: utf-8 -*-
# pylint: disable=R0915,W0201,W0611,R0902,I1101
from PyQt5 import QtCore, QtGui, QtWidgets
from Resources import Logo_rc

class Ui_MainWindow(QtWidgets.QWidget):
    """Initialization of GUI objects and assignment of their values."""
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
    def setupUi(self, MainWindow):
        """Initialization of GUI objects, positioning and naming."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 614)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1001, 571))
        self.tabWidget.setObjectName("tabWidget")

        # tab 1
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")

        self.headLabel_tab1 = QtWidgets.QLabel(self.tab_1)
        self.headLabel_tab1.setGeometry(QtCore.QRect(10, 0, 181, 21))
        self.headLabel_tab1.setStyleSheet("text-decoration: underline;\n"
                                          "font: 75 10pt \"Verdana\";")
        self.headLabel_tab1.setObjectName("headLabel_tab1")

        self.updateButton = QtWidgets.QPushButton(self.tab_1)
        self.updateButton.setGeometry(QtCore.QRect(160, 500, 111, 31))
        self.updateButton.setObjectName("updateButton")

        self.name_box_1 = QtWidgets.QLineEdit(self.tab_1)
        self.name_box_1.setGeometry(QtCore.QRect(10, 70, 121, 20))
        self.name_box_1.setText("")
        self.name_box_1.setObjectName("nameBox_tab1")

        self.path_box_1 = QtWidgets.QLineEdit(self.tab_1)
        self.path_box_1.setGeometry(QtCore.QRect(10, 130, 271, 20))
        self.path_box_1.setText("")
        self.path_box_1.setObjectName("path_box_1")

        self.logo_1 = QtWidgets.QLabel(self.tab_1)
        self.logo_1.setGeometry(QtCore.QRect(810, 20, 171, 111))
        self.logo_1.setObjectName("logo_1")

        self.results_label = QtWidgets.QLabel(self.tab_1)
        self.results_label.setGeometry(QtCore.QRect(10, 160, 51, 21))
        self.results_label.setObjectName("results_label")

        self.save_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.save_button_1.setGeometry(QtCore.QRect(810, 370, 161, 31))
        self.save_button_1.setObjectName("save_button_1")

        self.project_tab_1 = QtWidgets.QTableWidget(self.tab_1)
        self.project_tab_1.setGeometry(QtCore.QRect(810, 190, 161, 161))
        self.project_tab_1.setMaximumSize(QtCore.QSize(161, 16777215))
        self.project_tab_1.setObjectName("project_tab_1")
        self.project_tab_1.setColumnCount(1)
        self.project_tab_1.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.project_tab_1.setHorizontalHeaderItem(0, item)

        self.valueBox_tab1 = QtWidgets.QLineEdit(self.tab_1)
        self.valueBox_tab1.setGeometry(QtCore.QRect(470, 70, 113, 20))
        self.valueBox_tab1.setText("")
        self.valueBox_tab1.setObjectName("valueBox_tab1")

        self.pathLabel_tab1 = QtWidgets.QLabel(self.tab_1)
        self.pathLabel_tab1.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.pathLabel_tab1.setObjectName("pathLabel_tab1")

        self.projectLabel2_tab1 = QtWidgets.QLabel(self.tab_1)
        self.projectLabel2_tab1.setGeometry(QtCore.QRect(470, 100, 121, 21))
        self.projectLabel2_tab1.setObjectName("projectLabel2_tab1")

        self.para_combo_1 = QtWidgets.QComboBox(self.tab_1)
        self.para_combo_1.setGeometry(QtCore.QRect(320, 70, 111, 22))
        self.para_combo_1.setObjectName("para_combo_1")
        self.para_combo_1.addItem("")
        self.para_combo_1.addItem("")

        self.project_box_1 = QtWidgets.QLineEdit(self.tab_1)
        self.project_box_1.setGeometry(QtCore.QRect(470, 130, 121, 20))
        self.project_box_1.setText("")
        self.project_box_1.setObjectName("project_box_1")

        self.result_tab_1 = QtWidgets.QTableWidget(self.tab_1)
        self.result_tab_1.setGeometry(QtCore.QRect(10, 190, 761, 291))
        self.result_tab_1.setMinimumSize(QtCore.QSize(671, 0))
        self.result_tab_1.setObjectName("result_tab_1")
        self.result_tab_1.setRowCount(0)

        self.projectLabel3_tab1 = QtWidgets.QLabel(self.tab_1)
        self.projectLabel3_tab1.setGeometry(QtCore.QRect(810, 160, 91, 21))
        self.projectLabel3_tab1.setObjectName("projectLabel3_tab1")

        self.draw_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.draw_button_1.setGeometry(QtCore.QRect(810, 450, 161, 31))
        self.draw_button_1.setObjectName("draw_button_1")

        self.export_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.export_button_1.setGeometry(QtCore.QRect(10, 500, 111, 31))
        self.export_button_1.setObjectName("export_button_1")

        self.valueLabel_tab1 = QtWidgets.QLabel(self.tab_1)
        self.valueLabel_tab1.setGeometry(QtCore.QRect(470, 40, 91, 21))
        self.valueLabel_tab1.setObjectName("valueLabel_tab1")

        self.paraLabel_tab1 = QtWidgets.QLabel(self.tab_1)
        self.paraLabel_tab1.setGeometry(QtCore.QRect(320, 40, 91, 21))
        self.paraLabel_tab1.setObjectName("paraLabel_tab1")

        self.nameLabel_tab1 = QtWidgets.QLabel(self.tab_1)
        self.nameLabel_tab1.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.nameLabel_tab1.setObjectName("nameLabel_tab1")

        self.clear_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.clear_button_1.setGeometry(QtCore.QRect(810, 410, 161, 31))
        self.clear_button_1.setObjectName("clear_button_1")

        self.add_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.add_button_1.setGeometry(QtCore.QRect(310, 500, 111, 31))
        self.add_button_1.setObjectName("add_button_1")

        self.startButton = QtWidgets.QPushButton(self.tab_1)
        self.startButton.setGeometry(QtCore.QRect(660, 40, 111, 111))
        self.startButton.setObjectName("startButton")

        self.project_combo_1 = QtWidgets.QComboBox(self.tab_1)
        self.project_combo_1.setGeometry(QtCore.QRect(170, 70, 111, 22))
        self.project_combo_1.setObjectName("project_combo_1")

        self.projecLabel1_tab1 = QtWidgets.QLabel(self.tab_1)
        self.projecLabel1_tab1.setGeometry(QtCore.QRect(170, 40, 91, 21))
        self.projecLabel1_tab1.setObjectName("projecLabel1_tab1")
        self.tabWidget.addTab(self.tab_1, "")


        # tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.pid_button_2 = QtWidgets.QPushButton(self.tab_2)
        self.pid_button_2.setGeometry(QtCore.QRect(320, 130, 111, 21))
        self.pid_button_2.setObjectName("pid_button_2")

        self.pid_label_tab_2 = QtWidgets.QLabel(self.tab_2)
        self.pid_label_tab_2.setGeometry(QtCore.QRect(500, 15, 100, 25))
        self.pid_label_tab_2.setObjectName("pid_label_tab_2")

        self.pid_tab_2 = QtWidgets.QTableWidget(self.tab_2)
        self.pid_tab_2.setGeometry(QtCore.QRect(500, 40, 111, 111))
        self.pid_tab_2.setObjectName("pid_tab_2")
        self.pid_tab_2.setRowCount(0)

        self.logo_2 = QtWidgets.QLabel(self.tab_2)
        self.logo_2.setGeometry(QtCore.QRect(810, 20, 171, 111))
        self.logo_2.setObjectName("logo_2")

        self.export_button_2 = QtWidgets.QPushButton(self.tab_2)
        self.export_button_2.setGeometry(QtCore.QRect(10, 500, 111, 31))
        self.export_button_2.setObjectName("export_button_2")

        self.pathBox_tab2 = QtWidgets.QLineEdit(self.tab_2)
        self.pathBox_tab2.setGeometry(QtCore.QRect(10, 130, 271, 20))
        self.pathBox_tab2.setText("")
        self.pathBox_tab2.setObjectName("pathBox_tab2")

        self.result_tab_2 = QtWidgets.QTableWidget(self.tab_2)
        self.result_tab_2.setGeometry(QtCore.QRect(10, 190, 961, 291))
        self.result_tab_2.setMinimumSize(QtCore.QSize(671, 0))
        self.result_tab_2.setObjectName("result_tab_2")
        self.result_tab_2.setRowCount(0)

        self.resultsLabel_tab2 = QtWidgets.QLabel(self.tab_2)
        self.resultsLabel_tab2.setGeometry(QtCore.QRect(10, 160, 51, 21))
        self.resultsLabel_tab2.setObjectName("resultsLabel_tab2")

        self.head_label_tab2 = QtWidgets.QLabel(self.tab_2)
        self.head_label_tab2.setGeometry(QtCore.QRect(10, 0, 181, 21))
        self.head_label_tab2.setStyleSheet("text-decoration: underline;\n"
                                           "font: 75 10pt \"Verdana\";")
        self.head_label_tab2.setObjectName("head_label_tab2")

        self.updateButton_tab2 = QtWidgets.QPushButton(self.tab_2)
        self.updateButton_tab2.setGeometry(QtCore.QRect(160, 500, 111, 31))
        self.updateButton_tab2.setObjectName("updateButton_tab2")

        self.value_label_tab2 = QtWidgets.QLabel(self.tab_2)
        self.value_label_tab2.setGeometry(QtCore.QRect(810, 20, 171, 111))
        self.value_label_tab2.setObjectName("value_label_tab2")

        self.pathLabel_tab2 = QtWidgets.QLabel(self.tab_2)
        self.pathLabel_tab2.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.pathLabel_tab2.setObjectName("pathLabel_tab2")

        self.nameLabel_tab2 = QtWidgets.QLabel(self.tab_2)
        self.nameLabel_tab2.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.nameLabel_tab2.setObjectName("nameLabel_tab2")

        self.clearButton_tab2 = QtWidgets.QPushButton(self.tab_2)
        self.clearButton_tab2.setGeometry(QtCore.QRect(310, 500, 111, 31))
        self.clearButton_tab2.setObjectName("clearButton_tab2")

        self.name_box_2 = QtWidgets.QLineEdit(self.tab_2)
        self.name_box_2.setGeometry(QtCore.QRect(10, 70, 121, 20))
        self.name_box_2.setText("")
        self.name_box_2.setObjectName("name_box_2")

        self.start_button_2 = QtWidgets.QPushButton(self.tab_2)
        self.start_button_2.setGeometry(QtCore.QRect(660, 40, 111, 111))
        self.start_button_2.setObjectName("start_button_2")

        self.limit_button_2 = QtWidgets.QPushButton(self.tab_2)
        self.limit_button_2.setGeometry(QtCore.QRect(460, 500, 111, 31))
        self.limit_button_2.setObjectName("limit_button_2")

        self.paraLabel_tab2 = QtWidgets.QLabel(self.tab_2)
        self.paraLabel_tab2.setGeometry(QtCore.QRect(320, 40, 91, 21))
        self.paraLabel_tab2.setObjectName("paraLabel_tab2")

        self.para_combo_2 = QtWidgets.QComboBox(self.tab_2)
        self.para_combo_2.setGeometry(QtCore.QRect(320, 70, 111, 22))
        self.para_combo_2.setObjectName("para_combo_2")

        self.project_combo_2 = QtWidgets.QComboBox(self.tab_2)
        self.project_combo_2.setGeometry(QtCore.QRect(170, 70, 111, 22))
        self.project_combo_2.setObjectName("project_combo_2")

        self.projectLabel_tab2 = QtWidgets.QLabel(self.tab_2)
        self.projectLabel_tab2.setGeometry(QtCore.QRect(170, 40, 81, 21))
        self.projectLabel_tab2.setObjectName("projectLabel_tab2")

        self.tabWidget.addTab(self.tab_2, "")
        self.para_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.para_label_2.setGeometry(QtCore.QRect(860, 570, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.para_label_2.setFont(font)
        self.para_label_2.setObjectName("para_label_2")


        # tab 3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.logo_3 = QtWidgets.QLabel(self.tab_3)
        self.logo_3.setGeometry(QtCore.QRect(810, 20, 171, 111))
        self.logo_3.setObjectName("logo_3")

        self.name_box_3 = QtWidgets.QLineEdit(self.tab_3)
        self.name_box_3.setGeometry(QtCore.QRect(10, 70, 121, 20))
        self.name_box_3.setText("")
        self.name_box_3.setObjectName("name_box_3")

        self.pathLabel_tab3 = QtWidgets.QLabel(self.tab_3)
        self.pathLabel_tab3.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.pathLabel_tab3.setObjectName("pathLabel_tab3")

        self.path_box_3 = QtWidgets.QLineEdit(self.tab_3)
        self.path_box_3.setGeometry(QtCore.QRect(10, 130, 271, 20))
        self.path_box_3.setText("")
        self.path_box_3.setObjectName("path_box_3")

        self.results_label_3 = QtWidgets.QLabel(self.tab_3)
        self.results_label_3.setGeometry(QtCore.QRect(10, 160, 51, 21))
        self.results_label_3.setObjectName("results_label_3")

        self.result_tab_3 = QtWidgets.QTableWidget(self.tab_3)
        self.result_tab_3.setGeometry(QtCore.QRect(10, 190, 761, 291))
        self.result_tab_3.setMinimumSize(QtCore.QSize(671, 0))
        self.result_tab_3.setObjectName("resultTab_tab_3")
        self.result_tab_3.setRowCount(0)

        self.project_tab_3 = QtWidgets.QTableWidget(self.tab_3)
        self.project_tab_3.setGeometry(QtCore.QRect(810, 190, 161, 161))
        self.project_tab_3.setMaximumSize(QtCore.QSize(230, 16777215))
        self.project_tab_3.setObjectName("project_table_3")
        self.project_tab_3.setColumnCount(1)
        self.project_tab_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.project_tab_3.setHorizontalHeaderItem(0, item)

        self.headLabel_tab3 = QtWidgets.QLabel(self.tab_3)
        self.headLabel_tab3.setGeometry(QtCore.QRect(10, 0, 181, 21))
        self.headLabel_tab3.setStyleSheet("text-decoration: underline;\n"
                                          "font: 75 10pt \"Verdana\";")
        self.headLabel_tab3.setObjectName("headLabel_tab3")

        self.projectLabel2_tab3 = QtWidgets.QLabel(self.tab_3)
        self.projectLabel2_tab3.setGeometry(QtCore.QRect(470, 100, 121, 21))
        self.projectLabel2_tab3.setObjectName("projectLabel2_tab3")

        self.project_box_3 = QtWidgets.QLineEdit(self.tab_3)
        self.project_box_3.setGeometry(QtCore.QRect(470, 130, 121, 20))
        self.project_box_3.setText("")
        self.project_box_3.setObjectName("project_box_3")

        self.projectLabel3_tab3 = QtWidgets.QLabel(self.tab_3)
        self.projectLabel3_tab3.setGeometry(QtCore.QRect(810, 160, 91, 21))
        self.projectLabel3_tab3.setObjectName("projectLabel3_tab3")

        self.save_button_3 = QtWidgets.QPushButton(self.tab_3)
        self.save_button_3.setGeometry(QtCore.QRect(810, 370, 161, 31))
        self.save_button_3.setObjectName("save_button_3")

        # self.export_button_3 = QtWidgets.QPushButton(self.tab_3)
        # self.export_button_3.setGeometry(QtCore.QRect(10, 500, 111, 31))
        # self.export_button_3.setObjectName("export_button_3")

        self.nameLabel_tab3 = QtWidgets.QLabel(self.tab_3)
        self.nameLabel_tab3.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.nameLabel_tab3.setObjectName("nameLabel_tab3")

        self.clear_button_3 = QtWidgets.QPushButton(self.tab_3)
        self.clear_button_3.setGeometry(QtCore.QRect(810, 410, 161, 31))
        self.clear_button_3.setObjectName("clearButton_3")

        self.add_button_3 = QtWidgets.QPushButton(self.tab_3)
        self.add_button_3.setGeometry(QtCore.QRect(310, 500, 111, 31))
        self.add_button_3.setObjectName("add_button_3")

        self.start_button_3 = QtWidgets.QPushButton(self.tab_3)
        self.start_button_3.setGeometry(QtCore.QRect(660, 40, 111, 111))
        self.start_button_3.setObjectName("startButton")

        self.project_combo_3 = QtWidgets.QComboBox(self.tab_3)
        self.project_combo_3.setGeometry(QtCore.QRect(170, 70, 111, 22))
        self.project_combo_3.setObjectName("project_combo_3")

        self.projecLabel1_tab3 = QtWidgets.QLabel(self.tab_3)
        self.projecLabel1_tab3.setGeometry(QtCore.QRect(170, 40, 91, 21))
        self.projecLabel1_tab3.setObjectName("projecLabel1_tab3")

        self.voltage_box = QtWidgets.QLineEdit(self.tab_3)
        self.voltage_box.setGeometry(QtCore.QRect(320, 70, 113, 22))
        self.voltage_box.setText("")
        self.voltage_box.setObjectName("voltage_box")

        self.voltage_lable_3 = QtWidgets.QLabel(self.tab_3)
        self.voltage_lable_3.setGeometry(QtCore.QRect(320, 40, 91, 21))
        self.voltage_lable_3.setObjectName("voltage_lable_3")

        self.volume_box = QtWidgets.QLineEdit(self.tab_3)
        self.volume_box.setGeometry(QtCore.QRect(470, 70, 113, 20))
        self.volume_box.setText("")
        self.volume_box.setObjectName("volume_box")

        self.volume_lable_3 = QtWidgets.QLabel(self.tab_3)
        self.volume_lable_3.setGeometry(QtCore.QRect(470, 40, 113, 21))
        self.volume_lable_3.setObjectName("volume_lable_3")

        self.draw_button_3 = QtWidgets.QPushButton(self.tab_3)
        self.draw_button_3.setGeometry(QtCore.QRect(810, 450, 161, 31))
        self.draw_button_3.setObjectName("draw_button_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.updateButton.setText(_translate("MainWindow", "Update Table"))
        self.logo_1.setText(_translate("MainWindow", "<html><head/><body><p>"
                                       "<img src=\":/newPrefix/KIT.png\"/></p>"
                                       "</body></html>"))
        self.results_label.setText(_translate("MainWindow", "Results"))
        self.save_button_1.setText(_translate("MainWindow", "Save Project"))
        item = self.project_tab_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Project Item"))
        self.headLabel_tab1.setText(_translate("MainWindow", "ALiBaVa Search Tool"))
        self.pathLabel_tab1.setText(_translate("MainWindow", "Output path"))
        self.projectLabel2_tab1.setText(_translate("MainWindow", "Project Name"))
        self.para_combo_1.setItemText(0, _translate("MainWindow", "Voltage"))
        self.para_combo_1.setItemText(1, _translate("MainWindow", "Annealing"))
        self.projectLabel3_tab1.setText(_translate("MainWindow", "Current Project"))
        self.draw_button_1.setText(_translate("MainWindow", "Draw Project"))
        self.export_button_1.setText(_translate("MainWindow", "Export to File"))
        self.valueLabel_tab1.setText(_translate("MainWindow", "Parameter Value"))
        self.paraLabel_tab1.setText(_translate("MainWindow", "Search Parameter"))
        self.nameLabel_tab1.setText(_translate("MainWindow", "Sensor Name"))
        self.clear_button_1.setText(_translate("MainWindow", "Clear Project"))
        self.add_button_1.setText(_translate("MainWindow", ">> Add to Project"))
        self.startButton.setText(_translate("MainWindow", "Start Search"))
        self.projecLabel1_tab1.setText(_translate("MainWindow", "Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1),
                                  _translate("MainWindow",
                                             "ALiBaVa Search Tool"))

        # tab 2
        self.logo_2.setText(_translate("MainWindow", "<html><head/><body><p>"
                                       "<img src=\":/newPrefix/KIT.png\"/></p>"
                                       "</body></html>"))
        self.export_button_2.setText(_translate("MainWindow", "Export"))
        self.resultsLabel_tab2.setText(_translate("MainWindow", "Results"))
        self.head_label_tab2.setText(_translate("MainWindow", "Strip Mean Calculator"))
        self.updateButton_tab2.setText(_translate("MainWindow", "Update"))
        self.pathLabel_tab2.setText(_translate("MainWindow", "Output path"))
        self.nameLabel_tab2.setText(_translate("MainWindow", "Sensor Name"))
        self.clearButton_tab2.setText(_translate("MainWindow", "Clear"))
        self.start_button_2.setText(_translate("MainWindow", "Start Search"))
        self.limit_button_2.setText(_translate("MainWindow", "Limits"))
        self.paraLabel_tab2.setText(_translate("MainWindow", "Search Parameter"))
        self.pid_label_tab_2.setText(_translate("MainWindow", "PID List"))
        self.pid_button_2.setText(_translate("MainWindow", "Load PID List"))

        self.projectLabel_tab2.setText(_translate("MainWindow", "Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow",
                                             "Strip Mean Calculator"))
        self.para_label_2.setText(_translate("MainWindow", "Created by Marius Metzler"))

        # tab 3
        self.results_label_3.setText(_translate("MainWindow", "Results"))
        item = self.project_tab_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Project Item_3"))
        self.logo_3.setText(_translate("MainWindow", "<html><head/><body>"
                                       "<p><img src=\":/newPrefix/KIT.png\"/>"
                                       "</p></body></html>"))
        self.headLabel_tab3.setText(_translate("MainWindow", "Alpha Calculator"))
        self.pathLabel_tab3.setText(_translate("MainWindow", "Output path"))
        # self.export_button_3.setText(_translate("MainWindow", "Export to File"))
        self.save_button_3.setText(_translate("MainWindow", "Save Project"))
        self.projectLabel2_tab3.setText(_translate("MainWindow", "Project Name"))
        self.projectLabel3_tab3.setText(_translate("MainWindow", "Current Project"))
        self.volume_lable_3.setText(_translate("MainWindow", "Sample Volume (cm^3)"))
        self.voltage_lable_3.setText(_translate("MainWindow", "Target Voltage"))
        self.nameLabel_tab3.setText(_translate("MainWindow", "Sensor Name"))
        self.clear_button_3.setText(_translate("MainWindow", "Clear Project"))
        self.add_button_3.setText(_translate("MainWindow", ">> Add to Project"))
        self.start_button_3.setText(_translate("MainWindow", "Start Search"))
        self.draw_button_3.setText(_translate("MainWindow", "Draw Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  _translate("MainWindow",
                                             "Alpha Calculator"))
