from PyQt5 import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys


class App(QWidget):
    # Main Screen areas
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.resize(1920, 1080)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    c = a.palette()
    c.setBrush(QPalette.Background, QBrush(
        QPixmap("Assets/Loading_Screen.png")))
    a.setPalette(c)
    a.show()
    sys.exit(app.exec_())
