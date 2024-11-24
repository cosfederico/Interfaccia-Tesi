from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage

import os

class IntroPage(QWidget):
    
    readyClicked = pyqtSignal()
    exitClicked = pyqtSignal()
    
    def __init__(self, parent, title, text, button_text="Avanti", bottom_text="", warning_text="", error_text=""):
        super().__init__()
        self.parent_window = parent
        self.title_str = title
        self.text_str = text
        self.error_text_str = error_text
        self.warning_text_str = warning_text
        self.button_text = button_text
        
        self.setupUi()
        self.setContentsMargins(200,50,200,10)
        
        self.title.setText(self.title_str)
        self.text.setText(self.text_str)
        self.text.setWordWrap(True)
        self.bottom_text.setText(bottom_text)
        self.bottom_text.setWordWrap(True)
        self.warning_text.setText(self.warning_text_str)
        self.warning_text.setWordWrap(True)
        self.ready_button.setText(self.button_text)
        self.error_text.setText("")
        
        self.warning_icon.setPixmap(QPixmap.fromImage(QImage(os.path.join('GUI', 'icons', 'warning.png'))).scaledToWidth(self.warning_frame.geometry().width()))
        
        self.checkbox.toggled.connect(self.checkbox_toggled)
        self.ready_button.clicked.connect(self.ready_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)
    
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
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy)
        self.text.setMinimumSize(QSize(0, 300))
        self.text.setStyleSheet("font: 18pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.warning_frame = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warning_frame.sizePolicy().hasHeightForWidth())
        self.warning_frame.setSizePolicy(sizePolicy)
        self.warning_frame.setStyleSheet("border-radius: 10px;\n"
"background-color: rgb(255, 190, 190);")
        self.warning_frame.setFrameShape(QFrame.StyledPanel)
        self.warning_frame.setFrameShadow(QFrame.Raised)
        self.warning_frame.setObjectName("warning_frame")
        self.horizontalLayout_2 = QHBoxLayout(self.warning_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.warning_icon = QLabel(self.warning_frame)
        self.warning_icon.setText("")
        self.warning_icon.setObjectName("warning_icon")
        self.horizontalLayout_2.addWidget(self.warning_icon)
        spacerItem = QSpacerItem(30, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.warning_text = QLabel(self.warning_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warning_text.sizePolicy().hasHeightForWidth())
        self.warning_text.setSizePolicy(sizePolicy)
        self.warning_text.setStyleSheet("font: 15pt \"Rubik Light\";\n"
"color: rgb(255, 0, 0)")
        self.warning_text.setTextFormat(Qt.AutoText)
        self.warning_text.setObjectName("warning_text")
        self.horizontalLayout_2.addWidget(self.warning_text)
        self.verticalLayout.addWidget(self.warning_frame)
        self.error_text = QLabel(self)
        self.error_text.setMaximumSize(QSize(16777215, 30))
        self.error_text.setStyleSheet("font: 11pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255,0,0);")
        self.error_text.setObjectName("error_text")
        self.verticalLayout.addWidget(self.error_text)
        self.checkbox = QCheckBox(self)
        self.checkbox.setStyleSheet("font: 15pt \"Rubik Light\";")
        self.checkbox.setChecked(False)
        self.checkbox.setTristate(False)
        self.checkbox.setObjectName("checkbox")
        self.verticalLayout.addWidget(self.checkbox)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.exit_button = QPushButton(self)
        self.exit_button.setMinimumSize(QSize(300, 50))
        self.exit_button.setMaximumSize(QSize(300, 16777215))
        self.exit_button.setStyleSheet("border-radius: 10px;\n"
"font: 15pt \"Rubik Light\";\n"
"color: rgb(255,255,255);\n"
"background-color: rgb(0, 64, 130);")
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout.addWidget(self.exit_button)
        self.ready_button = QPushButton(self)
        self.ready_button.setMinimumSize(QSize(300, 50))
        self.ready_button.setMaximumSize(QSize(300, 16777215))
        self.ready_button.setStyleSheet("border-radius: 10px;\n"
"font: 15pt \"Rubik Light\";\n"
"color: rgb(255,255,255);\n"
"background-color: rgb(0, 64, 130);")
        self.ready_button.setObjectName("ready_button")
        self.horizontalLayout.addWidget(self.ready_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bottom_text = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_text.sizePolicy().hasHeightForWidth())
        self.bottom_text.setSizePolicy(sizePolicy)
        self.bottom_text.setMinimumSize(QSize(0, 0))
        self.bottom_text.setStyleSheet("font: 15pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.bottom_text.setAlignment(Qt.AlignCenter)
        self.bottom_text.setObjectName("bottom_text")
        self.verticalLayout.addWidget(self.bottom_text)
        self.checkbox.setText("Ho letto e compreso le informazioni riguardo questo studio e sono disposto a partecipare")
        self.exit_button.setText( "Esci")
        
    def checkbox_toggled(self):
        if self.sender().isChecked():
            self.error_text.setText("")
        
    def ready_button_clicked(self):
        if not self.checkbox.isChecked():
            self.error_text.setText(self.error_text_str)
            return
        
        self.readyClicked.emit()
        self.parent_window.next_page()
        self.parent_window.participant.add_answer(self.checkbox.text(), "Si", save_timestamp=False)
        
    def exit_button_clicked(self):
        self.exitClicked.emit()