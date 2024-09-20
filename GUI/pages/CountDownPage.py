from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

class CountDownPage(QWidget):
    
    def __init__(self, parent, seconds:int):
        super().__init__()
        self.parent_window = parent
        self.seconds = list(range(1, seconds))
        
        loadUi("GUI/qtdesigner/CountDownPage.ui", self)
        self.text.setText(str(seconds))
        
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