from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from datetime import datetime, timezone

class QuestionPage(QWidget):
    
    def __init__(self, parent, title, question):
        super().__init__()
        self.question_str = question
        self.title_str = title
                
        self.parent_window = parent
        
        loadUi("GUI/qtdesigner/QuestionPage.ui", self)
        self.question.setText(self.question_str)
        self.title.setText(self.title_str)
        self.next_button.clicked.connect(self.next_button_clicked)
        self.setContentsMargins(300,300,300,300)
            
    def next_button_clicked(self):
        self.parent_window.add_answer((self.inputbox.toPlainText(), datetime.now(timezone.utc).timestamp()))
        self.parent_window.next_page()