
from PyQt5 import QtGui
import pytesseract
import sys
import cv2
import re
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Instructions_Pop_up import Ui_MainWindow


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    # Main Screen areas
    def __init__(self):
        super().__init__()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.setWindowTitle("READEME")
        self.resize(3000, 3000)

        # Image area ---------------------------------------------------
        self.labelImage = QLabel(self)
        self.labelImage.setGeometry(QtCore.QRect(30, 50, 711, 470))
        self.labelImage.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.labelImage.setScaledContents(True)
        # Image area ---------------------------------------------------

        # Text area ------------------------------------------------------
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(1000, 50, 711, 470))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setObjectName("textEdit")
        # Text area ------------------------------------------------------

        # Webcam -------------------------------------------------------
        self.Webcam = QLabel(self)
        # self.Webcam.resize(640, 640)
        self.Webcam.setGeometry(QtCore.QRect(1040, 550, 711, 470))
        self.textLabel = QLabel('Webcam')
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        # Webcam -------------------------------------------------------

        # Buttons ------------------------------------------------------------
        self.Loadimage = QPushButton("Load Image", self)
        self.Loadimage.setObjectName("Load Image")
        self.Loadimage.setGeometry(QtCore.QRect(30, 610, 171, 41))
        self.Loadimage.resize(200, 50)
        self.Loadimage.setFont(QFont('Times', 15))
        self.Loadimage.clicked.connect(self.getImage)

        self.Run = QPushButton("Run", self)
        self.Run.setObjectName("Run")
        self.Run.setGeometry(QtCore.QRect(30, 660, 171, 41))
        self.Run.resize(200, 50)
        self.Run.setFont(QFont('Times', 15))
        self.Run.clicked.connect(self.extractText)

        self.Clear = QPushButton("Clear", self)
        self.Clear.setObjectName("Clear")
        self.Clear.setGeometry(QtCore.QRect(30, 710, 171, 41))
        self.Clear.resize(200, 50)
        self.Clear.setFont(QFont('Times', 15))
        self.Clear.clicked.connect(self.clearText)

        self.Save = QPushButton("Save text", self)
        self.Save.setObjectName("Save text")
        self.Save.setGeometry(QtCore.QRect(30, 760, 171, 41))
        self.Save.resize(200, 50)
        self.Save.setFont(QFont('Times', 15))
        self.Save.clicked.connect(self.saveText)

        self.Instructions = QPushButton("Instructions", self)
        self.Instructions.setObjectName("Instructions")
        self.Instructions.setGeometry(QtCore.QRect(30, 810, 171, 41))
        self.Instructions.resize(200, 50)
        self.Instructions.setFont(QFont('Times', 15))
        self.Instructions.clicked.connect(self.openWindow)

        self.Exit = QPushButton("Exit", self)
        self.Exit.setObjectName("Exit")
        self.Exit.setGeometry(QtCore.QRect(30, 860, 171, 41))
        self.Exit.resize(200, 50)
        self.Exit.setFont(QFont('Times', 15))
        self.Exit.clicked.connect(self.close)

        # Buttons ------------------------------------------------------------

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the Webcam with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.Webcam.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def close(self):
        exit()

    def getImage(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            options=options)
        # self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open a image", "","All Files (*);;Image Files (*.jpg);;Image Files (*.png)", options=options)
        if self.fileName:
            print(self.fileName)
            pattern = ".(jpg|png|jpeg|bmp|jpe|tiff)$"
            if re.search(pattern, self.fileName):
                self.setImage(self.fileName)

    def setImage(self, fileName):
        self.labelImage.setPixmap(QPixmap(fileName))
        self.Run.setEnabled(True)

    def extractText(self):
        config = ('-l eng --oem 1 --psm 3')
        img = cv2.imread(self.fileName, cv2.IMREAD_COLOR)
        # Run tesseract OCR on image
        text = pytesseract.image_to_string(img, config=config)
        # Print recognized text
        self.textEdit.append(text)
        print(text)

    def clearText(self):
        self.textEdit.clear()

    def saveText(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        # fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save text","All Files (*);;Text Files (*.txt)", options=options)
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(options=options)
        if fileName:
            print(fileName)
            file = open(fileName, 'w')
            text = self.textEdit.toPlainText()
            file.write(text)
            file.close()

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    c = a.palette()
    c.setColor(a.backgroundRole(), Qt.gray)
    a.setPalette(c)
    a.show()
    sys.exit(app.exec_())