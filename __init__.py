# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from . import gui
from PyQt5 import QtWidgets

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    mw.widget = QtWidgets.QMainWindow()
    result = gui.Ui_Form()
    result.setupUi(mw.widget)
    mw.widget.show()

# create a new menu item, "test"
action = QAction("drugi", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)