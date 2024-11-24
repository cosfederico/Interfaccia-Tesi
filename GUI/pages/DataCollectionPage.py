from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
import json

class DataCollectionPage(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent_window = parent
        
        self.setupUi()
        self.setContentsMargins(300,200,300,200)
        
        self.done_button.clicked.connect(self.done_button_clicked)
        self.error_text_str = self.error_text.text()
        self.error_text.setText("")
        
        with open(os.path.join('GUI', 'country.json')) as f:
            self.countries = json.load(f)

        self.countries = list(self.countries.values())
        self.nationality.addItems(self.countries)
        self.nationality.setCurrentIndex(self.countries.index("Italia"))
        
        self.nationality.setEditable(True)
        self.nationality.setInsertPolicy(QComboBox.NoInsert)
        self.nationality.completer().setCompletionMode(QCompleter.PopupCompletion)

    # Generated with QtDesigner
    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QLabel(self)
        self.title.setMaximumSize(QSize(500, 100))
        font = QFont()
        font.setFamily("Rubik Light")
        font.setPointSize(34)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.title.setFont(font)
        self.title.setStyleSheet("font: 34pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title, 0, Qt.AlignHCenter)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.groupBox = QGroupBox(self)
        self.groupBox.setMinimumSize(QSize(600, 300))
        self.groupBox.setMaximumSize(QSize(16777215, 200))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.age_label = QLabel(self.groupBox)
        self.age_label.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.age_label.setObjectName("age_label")
        self.horizontalLayout.addWidget(self.age_label)
        self.age = QLineEdit(self.groupBox)
        self.age.setMaximumSize(QSize(250, 16777215))
        self.age.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 14pt \"Rubik Light\";")
        self.age.setObjectName("age")
        self.horizontalLayout.addWidget(self.age)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gender_label = QLabel(self.groupBox)
        self.gender_label.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.gender_label.setObjectName("gender_label")
        self.horizontalLayout_2.addWidget(self.gender_label)
        self.gender = QComboBox(self.groupBox)
        self.gender.setMaximumSize(QSize(250, 16777215))
        self.gender.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);")
        self.gender.setObjectName("gender")
        self.gender.addItem("")
        self.gender.addItem("")
        self.horizontalLayout_2.addWidget(self.gender)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.nationality_label = QLabel(self.groupBox)
        self.nationality_label.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.nationality_label.setObjectName("nationality_label")
        self.horizontalLayout_5.addWidget(self.nationality_label)
        self.nationality = QComboBox(self.groupBox)
        self.nationality.setMaximumSize(QSize(250, 16777215))
        self.nationality.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);")
        self.nationality.setObjectName("nationality")
        self.horizontalLayout_5.addWidget(self.nationality)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.english_level_label = QLabel(self.groupBox)
        self.english_level_label.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.english_level_label.setObjectName("english_level_label")
        self.horizontalLayout_3.addWidget(self.english_level_label)
        self.english_level = QComboBox(self.groupBox)
        self.english_level.setMaximumSize(QSize(250, 16777215))
        self.english_level.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);\n"
"selection-color: rgb(255, 255, 255);")
        self.english_level.setObjectName("english_level")
        self.english_level.addItem("")
        self.english_level.addItem("")
        self.english_level.addItem("")
        self.english_level.addItem("")
        self.english_level.addItem("")
        self.english_level.addItem("")
        self.english_level.addItem("")
        self.horizontalLayout_3.addWidget(self.english_level)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox, 0, Qt.AlignHCenter)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.error_text = QLabel(self)
        self.error_text.setMaximumSize(QSize(16777215, 30))
        self.error_text.setStyleSheet("font: 10pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255,0,0);")
        self.error_text.setObjectName("error_text")
        self.verticalLayout_2.addWidget(self.error_text, 0, Qt.AlignHCenter)
        self.done_button = QPushButton(self)
        self.done_button.setMinimumSize(QSize(300, 50))
        self.done_button.setMaximumSize(QSize(200, 16777215))
        self.done_button.setStyleSheet("border-radius: 10px;\n"
"font: 15pt \"Rubik Light\";\n"
"color: rgb(255,255,255);\n"
"background-color: rgb(0, 64, 130);")
        self.done_button.setObjectName("done_button")
        self.verticalLayout_2.addWidget(self.done_button, 0, Qt.AlignHCenter)

        self.title.setText("Inserisci i tuoi dati")
        self.age_label.setText("Età")
        self.gender_label.setText("Genere")
        self.gender.setItemText(0, "M")
        self.gender.setItemText(1, "F")
        self.nationality_label.setText("Nazionalità")
        self.english_level_label.setText("Livello di Inglese")
        self.english_level.setItemText(0, "A1")
        self.english_level.setItemText(1, "A2")
        self.english_level.setItemText(2, "B1")
        self.english_level.setItemText(3, "B2")
        self.english_level.setItemText(4, "C1")
        self.english_level.setItemText(5, "C2")
        self.english_level.setItemText(6, "Madrelingua")
        self.done_button.setText( "Avanti")

    def done_button_clicked(self):
        age = self.age.text()
        gender = self.gender.currentText()
        english_level = self.english_level.currentText()
        nationality = self.nationality.currentText()
                            
        if (len(age)==0 or not nationality or not gender or not english_level):
            self.error_text.setText("Per favore compila tutti i campi.")
            return
        
        if nationality not in self.countries:
            self.error_text.setText("Per favore scegli una nazionalità valida.")
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
    