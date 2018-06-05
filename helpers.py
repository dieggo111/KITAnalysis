# pylint: disable=R1710, C0413, C0111, E0602, I1101, C0103, R0913, W0401
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def convert_dict(dic):
    """Convert all key and values of a data dict and its nested items into
    strings.
    """
    try:
        return {str(abs(round(key))): convert_value(val) for key, val in dic.items()}
    except TypeError:
        return {key: convert_value(val, key) for key, val in dic.items()}

def convert_list(lst):
    return [convert_value(item) for item in lst]

def convert_value(val, key=None):
    if isinstance(val, dict):
        return convert_dict(val)
    elif isinstance(val, list):
        return convert_list(val)
    elif isinstance(val, (int, float)):
        if key == "disc_ratio":
            return str(abs(round(val, 2)))
        elif 0 < abs(val) < 0.9:
            return "{:0.4e}".format(abs(val))
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
    """Adds header objects to TableWidget."""
    tab_obj.setColumnCount(count)
    for col in range(0, count):
        item = QtWidgets.QTableWidgetItem()
        item.setText(list(info_dict.keys())[col])
        tab_obj.setHorizontalHeaderItem(col, item)
    adjust_header(tab_obj, count, "Stretch")
    return True

def set_combo_box(combo_obj, project_list):
    """Adds items to QComboBox widget"""
    for i, pro in enumerate(project_list):
        combo_obj.addItem("")
        combo_obj.setItemText(i, pro)
