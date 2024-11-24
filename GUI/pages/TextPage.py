from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TextPage(QWidget):
    
    def __init__(self, parent, title, text, button_text="Avanti", button_slot=None):
        super().__init__()
        self.parent_window = parent
        self.title_str = title
        self.text_str = text
        self.button_text = button_text
        self.button_slot = button_slot
        
        self.setupUi()
        self.setContentsMargins(0,200,0,200)
        
        self.title.setText(self.title_str)
        self.text.setText(self.text_str)
        self.text.setWordWrap(True)
        self.ready_button.setText(self.button_text)
        
        if self.button_slot is not None:
            self.ready_button.clicked.connect(self.button_slot)
        else:
            self.ready_button.clicked.connect(self.ready_button_clicked)

    # Generated with QtDesigner    
    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QLabel(self)
        self.title.setStyleSheet("font: 38pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title, 0, Qt.AlignHCenter)
        self.text = QLabel(self)
        self.text.setMinimumSize(QSize(0, 300))
        self.text.setStyleSheet("font: 18pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text, 0, Qt.AlignHCenter)
        self.ready_button = QPushButton(self)
        self.ready_button.setMinimumSize(QSize(300, 50))
        self.ready_button.setMaximumSize(QSize(300, 16777215))
        self.ready_button.setStyleSheet("border-radius: 10px;\n"
"font: 15pt \"Rubik Light\";\n"
"color: rgb(255,255,255);\n"
"background-color: rgb(0, 64, 130);")
        self.ready_button.setObjectName("ready_button")
        self.verticalLayout.addWidget(self.ready_button, 0, Qt.AlignHCenter|Qt.AlignBottom)
        
    def ready_button_clicked(self):
        self.parent_window.next_page()