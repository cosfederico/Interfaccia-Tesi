from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

class RestPage(QWidget):
    
    def __init__(self, parent, text, wait_time):
        super().__init__()
        self.parent_window = parent
        self.text = text
        self.wait_time = wait_time
        
        loadUi("GUI/qtdesigner/RestPage.ui", self)
        self.label.setText(self.text)
        
    def showEvent(self, QShowEvent):
        self.play()
            
    def video_ended(self):
        self.parent_window.next_page()
        
    def play(self):
        if self.isVisible():
            QTimer.singleShot(self.wait_time * 1000, self.video_ended)  
