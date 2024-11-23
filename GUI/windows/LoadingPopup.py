from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

class LoadingPopup(QMessageBox):    
    def __init__(self, app: QApplication, message: str):
        super(LoadingPopup, self).__init__()
        self.app = app
        self.setWindowTitle("Interfaccia")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
        self.setText(message + "\t")
        self.setStandardButtons(QMessageBox.NoButton)
        self.show()
        self.app.processEvents()