from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

class TextPage(QWidget):
    
    def __init__(self, parent, title, text, button_text="Avanti", button_slot=None):
        super().__init__()
        self.parent_window = parent
        self.title_str = title
        self.text_str = text
        self.button_text = button_text
        self.button_slot = button_slot
        
        loadUi("GUI/qtdesigner/TextPage.ui", self)
        self.setContentsMargins(500,300,500,300)
        
        self.title.setText(self.title_str)
        self.text.setText(self.text_str)
        self.ready_button.setText(self.button_text)
        
        if self.button_slot is not None:
            self.ready_button.clicked.connect(self.button_slot)
        else:
            self.ready_button.clicked.connect(self.ready_button_clicked)
        
    def ready_button_clicked(self):
        self.parent_window.next_page()