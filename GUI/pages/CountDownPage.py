from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CountDownPage(QWidget):
    
    def __init__(self, parent, seconds:int):
        super().__init__()
        self.parent_window = parent
        self.seconds = list(range(1, seconds))
        
        self.setupUi()
        self.text.setText(str(seconds))
        
    # Generated with QtDesigner        
    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.text = QLabel(self)
        self.text.setStyleSheet("font: 80pt \"Rubik\";\n"
"color: rgb(200,200,200);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.text.setObjectName("text")
        self.gridLayout.addWidget(self.text, 0, 0, 1, 1, Qt.AlignHCenter)
        
    def showEvent(self, QShowEvent):
        self.play()
        
    def play(self):
        if self.isVisible():
            QTimer.singleShot(1000, self.tick)  
            
    def tick(self):
        try:
            self.text.setText(str(self.seconds.pop()))
            QTimer.singleShot(1000, self.tick)
        except:
            self.parent_window.next_page()