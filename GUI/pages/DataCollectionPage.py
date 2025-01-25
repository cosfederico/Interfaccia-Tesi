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
        self.setContentsMargins(0,200,0,200)
        
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

        self.occupation.setEditable(True)

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
        self.groupBox.setMinimumSize(QSize(1000, 300))
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
        self.age.setMaximumSize(QSize(400, 16777215))
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
        # self.gender.setMaximumSize(QSize(250, 16777215))
        self.gender.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);")
        self.gender.setObjectName("gender")
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
        # self.nationality.setMaximumSize(QSize(250, 16777215))
        self.nationality.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);")
        self.nationality.setObjectName("nationality")
        self.horizontalLayout_5.addWidget(self.nationality)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.education_label = QLabel(self.groupBox)
        self.education_label.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.education_label.setObjectName("education_label")
        self.horizontalLayout_3.addWidget(self.education_label)
        self.education = QComboBox(self.groupBox)
        # self.education.setMaximumSize(QSize(250, 16777215))
        self.education.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);\n"
"selection-color: rgb(255, 255, 255);")
        self.education.setObjectName("education")
        self.horizontalLayout_3.addWidget(self.education)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.occupation_label = QLabel(self.groupBox)
        self.occupation_label.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.occupation_label.setObjectName("occupation_label")
        self.horizontalLayout_4.addWidget(self.occupation_label)
        self.occupation = QComboBox(self.groupBox)
        # self.occupation.setMaximumSize(QSize(250, 16777215))
        self.occupation.setStyleSheet("font: 14pt \"Rubik Light\";\n"
"selection-background-color: rgb(0, 64, 130);\n"
"selection-color: rgb(255, 255, 255);")
        self.occupation.setObjectName("occupation")
        self.horizontalLayout_4.addWidget(self.occupation)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

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
        self.gender.addItem("Maschio")
        self.gender.addItem("Femmina")
        self.gender.addItem("Preferisco non specificarlo")
        self.nationality_label.setText("Nazionalità")
        self.education_label.setText("Titolo di studio")
        self.education.addItem("Licenza media")
        self.education.addItem("Diploma di scuola superiore")
        self.education.addItem("Laurea triennale")
        self.education.addItem("Laurea magistrale o ciclo unico")
        self.education.addItem("Dottorato o titolo superiore")
        self.education.addItem("Altro titolo")

        self.occupation_label.setText("Occupazione")
        self.occupation.addItem("")
        self.occupation.addItem("Disoccupato/a")
        self.occupation.addItem("Studente")
        self.occupation.addItem("Imprenditore")
        self.occupation.addItem("Lavoratore Indipendente")
        self.occupation.addItem("Libero professionista")

        self.done_button.setText( "Avanti")

        for i in range(self.education.count()):
                self.education.setItemData(i, self.education.itemText(i), Qt.ToolTipRole)

    def done_button_clicked(self):
        age = self.age.text()
        gender = self.gender.currentText()
        education = self.education.currentText()
        nationality = self.nationality.currentText()
        occupation = self.occupation.currentText()
                            
        if (len(age)==0 or len(occupation)==0 or not nationality or not gender or not education):
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
            if (age >= 18 and age < 100):
                self.parent_window.participant.set_data(age, gender, nationality, education, occupation)
                self.parent_window.next_page()
            else:
                self.error_text.setText("Inserire un'età valida.")
    