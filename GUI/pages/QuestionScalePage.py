from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from datetime import datetime, timezone

class QuestionScalePage(QWidget):
    
    def __init__(self, parent, title, question):
        super().__init__()
        self.question_str = question
        self.title_str = title
        self.parent_window = parent
        self.selected_answer = None
        
        loadUi("GUI/qtdesigner/QuestionScalePage.ui", self)
        self.setContentsMargins(200,300,200,300)
        self.next_button.clicked.connect(self.next_button_clicked)
        self.scale_1.toggled.connect(self.answer_clicked)
        self.scale_2.toggled.connect(self.answer_clicked)
        self.scale_3.toggled.connect(self.answer_clicked)
        self.scale_4.toggled.connect(self.answer_clicked)
        self.scale_5.toggled.connect(self.answer_clicked)
        
        self.question.setText(self.question_str)
        self.title.setText(self.title_str)
        
        self.error_text_str = self.error_text.text()
        self.error_text.setText("")
            
    def answer_clicked(self):
        rb = self.sender()
        if rb.isChecked():
            self.selected_answer = rb.text() 
            
    def next_button_clicked(self):
        if self.selected_answer is None:
            self.error_text.setText(self.error_text_str)
            return
            
        self.parent_window.participant.add_answer(self.question.text(), self.selected_answer)
        self.parent_window.next_page()