from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PANAS(QWidget):
    
    nextClicked = pyqtSignal(list, list, str)
    
    def __init__(self, parent, emotions:list, scale:list, flag="", error_text="Per rispondi a tutte le domande."):
        super().__init__()
        self.parent_window = parent
        self.error_text_str = error_text
        self.scale = scale        
        self.emotions = emotions
        self.flag = flag
        
        self.setupUi()
        self.setContentsMargins(100,100,100,100)
        self.next_button.clicked.connect(self.next_button_clicked)
        
    def next_button_clicked(self):
        emotions = []
        answers = []
            
        for button_group in self.button_groups:
            checked_button = button_group.checkedButton()
            
            if checked_button is None:
                self.error_text.setText(self.error_text_str)
                return
            
            emotions.append(button_group.objectName() + "_" + self.flag)
            answers.append(self.scale.index(checked_button.objectName())+1)
        
        self.nextClicked.emit(emotions, answers, "PANAS_" + self.flag)
        self.parent_window.next_page()
        
    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.verticalLayout = QVBoxLayout(self)
        
        self.title = QLabel(self)
        self.title.setStyleSheet("font: 30pt \"Rubik SemiBold\";\ncolor: rgb(0, 51, 102)")
        self.verticalLayout.addWidget(self.title)
        
        self.question = QLabel(self)
        self.question.setStyleSheet("font: 17pt \"Rubik light\";\ncolor: rgb(53, 53, 53)")
        self.question.setWordWrap(True)
        self.verticalLayout.addWidget(self.question)
        
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollVerticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        
        self.formLayout = QFormLayout()
        
        self.filler_label = QLabel(self.scrollAreaWidgetContents)
        self.filler_label.setText("")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.filler_label)
        
        self.LabelsHLayout = QHBoxLayout()
        
        for level in self.scale:
            label = QLabel(self.scrollAreaWidgetContents)
            label.setStyleSheet("font: 15pt \"Rubik Light\";")
            label.setObjectName(level)
            label.setText(level)
            self.LabelsHLayout.addWidget(label, 0, Qt.AlignHCenter)
        
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.LabelsHLayout)
                
        self.button_groups = []
        i = 1
        for emotion in self.emotions:
            
            line = QFrame(self.scrollAreaWidgetContents)
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            if i == 1:
                line.setMidLineWidth(2)
            self.formLayout.setWidget(i, QFormLayout.FieldRole, line)
            i += 1
            
            label = QLabel(self.scrollAreaWidgetContents)
            label.setStyleSheet("font: 15pt \"Rubik Light\";")
            label.setObjectName(emotion)
            label.setText(emotion)
            label.setMargin(15)
            self.formLayout.setWidget(i, QFormLayout.LabelRole, label)
            
            hLayout = QHBoxLayout()
            
            button_group = QButtonGroup(self)
            button_group.setObjectName(emotion)
            
            for level in self.scale:
                rb = QRadioButton(self)
                rb.setObjectName(level)
                rb.setStyleSheet('QRadioButton::indicator { width: 20px; height: 20px;};')
                rb.setText("")
                hLayout.addWidget(rb, 0, Qt.AlignCenter)
                button_group.addButton(rb)
                
            self.formLayout.setLayout(i, QFormLayout.FieldRole, hLayout)
            self.button_groups.append(button_group)
            i += 1
        
        self.scrollVerticalLayout.addLayout(self.formLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        
        self.buttons_layout = QHBoxLayout()
        
        self.error_text = QLabel(self)
        self.error_text.setMaximumSize(QSize(16777215, 30))
        self.error_text.setStyleSheet("font: 10pt \"Rubik Light\";\nbackground-color: rgba(255, 255, 255, 0);\ncolor: rgb(255,0,0);")
        self.buttons_layout.addWidget(self.error_text, 0, Qt.AlignRight)
        
        self.next_button = QPushButton(self)
        self.next_button.setMinimumSize(QSize(300, 50))
        self.next_button.setMaximumSize(QSize(250, 16777215))
        self.next_button.setStyleSheet("border-radius: 10px;\nfont: 15pt \"Rubik Light\";\ncolor: rgb(255,255,255);\nbackground-color: rgb(0, 64, 130);")
        self.buttons_layout.addWidget(self.next_button)
        
        self.verticalLayout.addLayout(self.buttons_layout)

        self.setTextUI()

    def setTextUI(self):
        self.title.setText("PANAS")
        self.question.setText("Questa scala consiste in una serie di parole che descrivono differenti sentimenti ed emozioni.\nLeggi ciascun item e seleziona, tra le opzioni disponibili accanto alla parola, la risposta appropriata che descrive come ti senti in questo esatto momento.")
        self.error_text.setText("")
        self.next_button.setText("Avanti")
