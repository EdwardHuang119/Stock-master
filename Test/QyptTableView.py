#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
# from Test.TushareProApi import Getdailyfromconcept, Getconcept

'''''''''
def QyTalbeShow(data):
    class pandasModel(QAbstractTableModel):

        def __init__(self, data):
            QAbstractTableModel.__init__(self)
            self._data = data

        def rowCount(self, parent=None):
            return self._data.shape[0]

        def columnCount(self, parnet=None):
            return self._data.shape[1]

        def data(self, index, role=Qt.DisplayRole):
            if index.isValid():
                if role == Qt.DisplayRole:
                    return str(self._data.iloc[index.row(), index.column()])
            return None

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self._data.columns[col]
            return None


''''''''''''''
df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})
'''''''''''
# df = Getdailyfromconcept('TS355', 20191009, 20191010)
# df = Getconcept('')

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data


    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


def Dataframdatashow(data):
    app = QApplication(sys.argv)
    model = pandasModel(data)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())

# Talbe1 = Dataframdatashow(df)

''''''''''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
'''''