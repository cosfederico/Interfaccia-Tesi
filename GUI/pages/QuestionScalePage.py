from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class QuestionScalePage(QWidget):
        
    def __init__(self, parent, title, question, scale=["Per niente", "Poco", "Abbastanza", "Molto", "Moltissimo"], error_text="Per favore scegli una risposta."):
        super().__init__()
        self.parent_window = parent
        self.question_str = question
        self.title_str = title
        self.scale = scale
        self.error_text_str = error_text
        self.selected_answer = None
                
        self.setupUi()
        self.setContentsMargins(200,300,200,300)
        self.next_button.clicked.connect(self.next_button_clicked)

    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(self)
        
        self.title = QLabel(self)
        self.title.setStyleSheet("font: 30pt \"Rubik SemiBold\";\n"
                "color: rgb(0, 51, 102);\n"
                "background-color: rgba(255, 255, 255, 0);\n"
                "")
        self.title.setText(self.title_str)
        self.verticalLayout.addWidget(self.title)

        self.question = QLabel(self)
        self.question.setStyleSheet("font: 20pt \"Rubik light\";\n"
                "color: rgb(53, 53, 53);\n"
                "background-color: rgba(255, 255, 255, 0);")
        self.question.setText(self.question_str)
        self.verticalLayout.addWidget(self.question)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        self.answer_layout = QHBoxLayout()
        
        for level in self.scale:
                rb = QRadioButton(self)
                rb.setStyleSheet("font: 16pt \"Rubik Light\";")
                rb.setObjectName(level)
                rb.setText(level)
                rb.toggled.connect(self.answer_clicked)
                self.answer_layout.addWidget(rb)
        
        self.verticalLayout.addLayout(self.answer_layout)
        
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        
        self.horizontalLayout_2 = QHBoxLayout()

        self.error_text = QLabel(self)
        self.error_text.setMaximumSize(QSize(16777215, 30))
        self.error_text.setStyleSheet("font: 10pt \"Rubik Light\";\n"
                "background-color: rgba(255, 255, 255, 0);\n"
                "color: rgb(255,0,0);")
        self.error_text.setText("")
        self.horizontalLayout_2.addWidget(self.error_text, 0, Qt.AlignRight)
        
        self.next_button = QPushButton(self)
        self.next_button.setMinimumSize(QSize(300, 50))
        self.next_button.setMaximumSize(QSize(250, 16777215))
        self.next_button.setStyleSheet("border-radius: 10px;\n"
                "font: 15pt \"Rubik Light\";\n"
                "color: rgb(255,255,255);\n"
                "background-color: rgb(0, 64, 130);")
        self.next_button.setText("Avanti")
        self.horizontalLayout_2.addWidget(self.next_button)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

    def answer_clicked(self):
        rb = self.sender()
        if rb.isChecked():
            self.selected_answer = rb.text() 
            
    def next_button_clicked(self):
        if self.selected_answer is None:
            self.error_text.setText(self.error_text_str)
            return
            
        self.parent_window.participant.add_answer(self.question.text(), self.scale.index(self.selected_answer)+1)
        self.parent_window.next_page()    
