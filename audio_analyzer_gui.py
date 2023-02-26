#  date: 26. 02. 2023
#  author: Daniel Schnurpfeil
#

import sys

from PySide6 import QtWidgets

from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("AUdio segments analyzer")
    window.show()
    window.activateWindow()
    window.raise_()
    app.exec()
