from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.pages.QuestionPage import *

class Poll(QWidget):
    
    def __init__(self, parent, questions):
        super().__init__()
        self.parent_window = parent
        self.questions = questions
        self.answers = []
        
        self.setupUI()

    def setupUI(self):
        self.stacked_widget = QStackedWidget()
        
        for i, question in enumerate(self.questions):
            self.stacked_widget.addWidget(QuestionPage(self, "Domanda " + str(i+1), question))  
            
        self.initialLayout = QHBoxLayout()
        self.initialLayout.addWidget(self.stacked_widget)
                    
        self.setLayout(self.initialLayout)
        
    def add_answer(self, answer:str):
        self.answers.append(answer)
        
    def next_page(self):
        if (self.stacked_widget.currentIndex() == len(self.questions)-1):
            self.poll_ended()
            
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
    
    def showEvent(self, QShowEvent):
        if self.stacked_widget.currentIndex() == -1:
            self.poll_ended()
    
    def poll_ended(self):
        self.parent_window.subject.add_video_answers(self.answers)
        self.parent_window.next_page()