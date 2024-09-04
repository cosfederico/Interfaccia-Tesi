from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import os
import csv

class WelcomePage(QWidget):
    
    def __init__(self, parent, title, text, button_text):
        super(WelcomePage, self).__init__()
        self.parent_window = parent
        self.title = title
        self.text = text
        self.button_text = button_text
        
        self.setupUI()
        
    def setupUI(self): 
        loadUi("GUI/qtdesigner/WelcomePage.ui", self)
        self.setContentsMargins(300,300,300,300)
        
        self.title_label.setText(self.title)
        self.text_label.setText(self.text)
        self.ready_button.setText(self.button_text)
        
        self.ready_button.clicked.connect(self.ready_button_clicked)
        self.browse_button.clicked.connect(self.browse_button_clicked)
        
    def browse_button_clicked(self):
        url = QFileDialog.getOpenFileUrl(self, "Select Real Video", QUrl(""), "CSV files (*.csv)")
        self.path_text_label.setText(url[0].url().split("///")[1])
        
    def ready_button_clicked(self):
        path = self.path_text_label.text()
        if len(path) != 0: 
            if (os.path.isfile(path)):
                print(path)
                self.parent_window.load_protocol_file(path)         
                self.next_page()

        self.error_text_label.setText("Seleziona un file valido.")
            
    def next_page(self):
        self.parent_window.next_page()