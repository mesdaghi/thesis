'''
Instantiate our custom main window class using the layout in the ui file (created with qt designer)
'''

# Make the imports
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint
import sys
import os


app = QtWidgets.QApplication(sys.argv)
# Initiate qdialog
window = QtWidgets.QMainWindow()

# Load form from ui file
uifile = "/home/filo/PycharmProjects/CONpyMOL/contacts_qtwidget.ui"
form = loadUi(uifile, window)


def clicked():
    model = form.MoleculeSelectionListView.model()
    print("CLICKED!")
    print(form.actionShow_all.isChecked())
    #for index in range(model.rowCount()):
    #    item = model.item(index)
    #    print(item)
    #    if item.checkState() == Qt.Checked:
    #        print(item.text())


form.actionOpen_cmap.triggered.connect(clicked)


model = QStandardItemModel(form.MoleculeSelectionListView)
for n in range(10):
    item = QStandardItem('Item %s' % randint(1, 100))
    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

    check = Qt.Checked if randint(0, 1) == 1 else Qt.Unchecked

    item.setData(QVariant(check), Qt.CheckStateRole)
    model.appendRow(item)

form.MoleculeSelectionListView.setModel(model)
print(model.rowCount())

# Show dialog window
window.show()
sys.exit(app.exec_())



