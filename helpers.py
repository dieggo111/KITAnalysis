# pylint: disable=R1710, C0413, C0111, E0602, I1101, C0103, R0913, W0401
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def read_table(tab_obj, sort="col"):
    """Reads content of table and puts it in dict.

    Args:
        - tab_obj (QTableWidget) : table object
        - sort (str) : if 'col' then dict keys are column names, if 'row' they
                       are sorted by row
    """
    dic = {}
    if sort == "col":
        for col in range(0, tab_obj.columnCount()):
            name = tab_obj.horizontalHeaderItem(col).text()
            dic[name] = []
            for row in range(0, tab_obj.rowCount()):
                dic[name].append(float(tab_obj.item(row, col).text()))
    if sort == "row":
        for row in range(0, tab_obj.rowCount()):
            name = tab_obj.verticalHeaderItem(row).text()
            dic[name] = []
            for col in range(0, tab_obj.columnCount()):
                dic[name].append(float(tab_obj.item(row, col).text()))
    return dic

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

def add_header(tab_obj, count, name, hv="horizontal"):
    """Adds header objects to TableWidget.

    Args:
        - tab_obj (QTableWidget) : table object
        - count (int) : number of cells
        - name (str) : header name
        - hv (str) : choose horizontal or vertical header
    """
    tab_obj.setColumnCount(count)
    for col in range(0, count):
        item = QtWidgets.QTableWidgetItem()
        if isinstance(name, dict):
            item.setText(list(name.keys())[col])
        if isinstance(name, list):
            item.setText(name[col])
        if hv == "horizontal":
            tab_obj.setHorizontalHeaderItem(col, item)
            adjust_header(tab_obj, count, "Stretch")
        if hv == "vertical":
            tab_obj.setVerticalHeaderItem(col, item)
    return True

def set_combo_box(combo_obj, project_list):
    """Adds items to QComboBox widget"""
    for i, pro in enumerate(project_list):
        combo_obj.addItem("")
        combo_obj.setItemText(i, pro)
