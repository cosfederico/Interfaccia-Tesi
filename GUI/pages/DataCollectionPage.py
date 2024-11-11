from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

import os
import json

class DataCollectionPage(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent_window = parent
        
        loadUi("GUI/qtdesigner/DataCollectionPage.ui", self)
        self.setContentsMargins(300,200,300,200)
        
        self.done_button.clicked.connect(self.done_button_clicked)
        self.error_text_str = self.error_text.text()
        self.error_text.setText("")
        
        with open(os.path.join('GUI', 'country.json')) as f:
            countries = json.load(f)

        countries = list(countries.values())
        self.nationality.addItems(countries)
        self.nationality.setCurrentIndex(countries.index("Italia"))
              
    def done_button_clicked(self):
        age = self.age.text()
        gender = self.gender.currentText()
        english_level = self.english_level.currentText()
        nationality = self.nationality.currentText()
                
        if (len(age)==0 or not nationality or not gender or not english_level):
            self.error_text.setText("Per favore compila tutti i campi.")
            return
        
        try:
            age = int(age)
        except:
            self.error_text.setText("Inserire un'età valida.")
        else:
            if (age > 18 and age < 100):
                self.parent_window.participant.set_data(age, gender, nationality, english_level)
                self.parent_window.next_page()
            else:
                self.error_text.setText("Inserire un'età valida.")
    