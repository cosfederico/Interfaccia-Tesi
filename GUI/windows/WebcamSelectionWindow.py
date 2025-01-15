from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.uic import loadUi

from GUI.windows.WebcamPreviewWindow import *

import cv2
import sys

class CameraBox(QGroupBox):
    selected = pyqtSignal(QWidget)
    deselected = pyqtSignal(QWidget)
    
    def __init__(self, cap:cv2.VideoCapture, id=0, parent=None):
        super(CameraBox, self).__init__(parent)
        self.cap = cap
        self.id = id
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.isSelected = False
        
        self.setupUi()
        
        if self.fps > 0:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(int(1e3/self.fps))
        
    def setupUi(self):
        box_layout = QVBoxLayout()
        self.frame = QLabel()
        self.update_frame()
        box_layout.addWidget(self.frame, alignment=Qt.AlignCenter)
        box_layout.addWidget(QLabel("Webcam %d (%d x %d)" %(self.id, self.frame_width, self.frame_height)), alignment=Qt.AlignCenter)
        self.setLayout(box_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.select(not self.isSelected)
        super(CameraBox, self).mousePressEvent(event)
        
    def select(self, select):
        if select:
            self.selected.emit(self)
            self.setStyleSheet("background-color: rgb(253,255,157)")
            self.isSelected = True
        else:
            self.deselected.emit(self)
            self.setStyleSheet("")
            self.isSelected = False
            
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            bytesPerLine = 3 * self.frame_width
            self.frame.setPixmap(QPixmap.fromImage(QImage(frame.data, self.frame_width, self.frame_height, bytesPerLine, QImage.Format_BGR888)).scaledToHeight(256))
    
    def release_resources(self):
        try:
            self.timer.stop()
        except:
            pass
        self.cap.release()
    
class WebcamSelectionWindow(QDialog):
    
    capSelected = pyqtSignal(cv2.VideoCapture, int)
        
    def __init__(self, app, text="Scegli la webcam da utilizzare per la cattura del volto", text2="Premi il pulsante sottostante per verificare che l'audio funzioni correttamente", text3="Se non senti nessun suono premendo il bottone, verifica il dispositivo audio in uso, e riprova prima di cominciare.", error_text="Scegli una webcam per cominciare."):
        super().__init__()
        
        self.app = app
        self.text_str = text
        self.text2_str = text2
        self.text3_str = text3
        self.error_text_str = error_text
        self.boxes = []
        self.selected_box = None
                        
        self.setupUi()
        self.setContentsMargins(50,50,50,50)
        self.setWindowTitle("Selezione Webcam")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons','webcam.png')))
                
        self.text.setText(self.text_str)
        self.text2.setText(self.text2_str)
        self.text3.setText(self.text3_str)
        self.error_text.setText("")
        self.done_button.clicked.connect(self.done_button_clicked)
        self.audio_button.clicked.connect(self.play)
        
        audio_test_file = os.path.join('GUI', 'sounds', 'test.mp3')
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_content = QMediaContent(QUrl.fromLocalFile(audio_test_file))
        self.player.setMedia(self.media_content)
        self.player.setVolume(100)
                            
        self.load_cams()
                
    # Generated with QtDesigner
    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QLabel(self)
        self.title.setStyleSheet("font: 30pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title, 0, Qt.AlignHCenter)
        self.text = QLabel(self)
        self.text.setStyleSheet("font: 17pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text, 0, Qt.AlignHCenter)
        self.box = QGroupBox(self)
        self.box.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setFamily("Rubik Light")
        font.setPointSize(10)
        font.setItalic(True)
        self.box.setFont(font)
        self.box.setTitle("")
        self.box.setObjectName("box")
        self.verticalLayout.addWidget(self.box)
        spacerItem = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)
        self.text2 = QLabel(self)
        self.text2.setStyleSheet("font: 17pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.text2.setObjectName("text2")
        self.verticalLayout.addWidget(self.text2, 0, Qt.AlignHCenter)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.audio_button = QPushButton(self)
        self.audio_button.setMinimumSize(QSize(0, 0))
        self.audio_button.setStyleSheet("font: 11pt \"Rubik Light\";\n"
"background-color: rgb(250, 250, 250);")
        self.audio_button.setCheckable(False)
        self.audio_button.setObjectName("audio_button")
        self.horizontalLayout.addWidget(self.audio_button, 0, Qt.AlignRight)
        self.audio_icon = QLabel(self)
        self.audio_icon.setText("")
        self.audio_icon.setObjectName("audio_icon")
        self.horizontalLayout.addWidget(self.audio_icon, 0, Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.text3 = QLabel(self)
        self.text3.setStyleSheet("font: 17pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.text3.setObjectName("text3")
        self.verticalLayout.addWidget(self.text3, 0, Qt.AlignHCenter)
        spacerItem1 = QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.error_text = QLabel(self)
        self.error_text.setStyleSheet("font: 13pt \"Rubik Light\";\n"
"color: rgb(255, 0, 0)")
        self.error_text.setText("")
        self.error_text.setObjectName("error_text")
        self.verticalLayout.addWidget(self.error_text, 0, Qt.AlignHCenter)
        self.done_button = QPushButton(self)
        self.done_button.setMinimumSize(QSize(200, 50))
        self.done_button.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 64, 130);\n"
"font: 14pt \"Rubik Light\";\n"
"color: rgb(255,255,255);")
        self.done_button.setObjectName("done_button")
        self.verticalLayout.addWidget(self.done_button, 0, Qt.AlignHCenter)

        self.title.setText("Prima di iniziare")
        self.audio_button.setText("Prova audio")
        self.done_button.setText("Fatto")
        
    def media_status_changed(self, state):
        if state == QMediaPlayer.EndOfMedia:
            self.audio_icon.clear()
        
    def load_cams(self):
        
        cams, cams_ids = self.get_working_webcams()
        
        if len(cams) == 0:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
            error_msg.setWindowTitle("Interfaccia")
            error_msg.setText("Nessuna webcam disponibile trovata.\nAssicurati di avere almeno una webcam collegata al computer, non in uso da un altro programma.")
            error_msg.exec_()
            sys.exit()
            
        videos_layout = QGridLayout()
        
        i = 0
        for cam, id in zip(cams, cams_ids):
            box = CameraBox(cam, id=id)
            box.selected.connect(self.box_selected)   
            box.deselected.connect(self.box_deselected)   
            self.boxes.append(box)
            videos_layout.addWidget(box, i/3, i%3, alignment=Qt.AlignTop)
            i += 1
        
        self.box.setLayout(videos_layout)
        
    def box_selected(self, selected_box):
        for box in self.boxes:
            if box.isSelected:
                box.select(False)
        self.selected_box = selected_box
        self.error_text.setText("")
        
    def box_deselected(self):
        self.selected_box = None
        
    def done_button_clicked(self):
        
        if not self.selected_box:
            self.error_text.setText(self.error_text_str)
            return
        
        for box in self.boxes:
            if box != self.selected_box:
                box.release_resources()
        
        try:
            self.selected_box.timer.stop()
        except:
            pass

        self.capSelected.emit(self.selected_box.cap, self.selected_box.id)
        self.close()
        
    def get_working_webcams(self):

        camera_idx = 0
        cams = []
        cams_ids = []
        
        while True:
            camera = cv2.VideoCapture(camera_idx)
            if not camera.isOpened():
                break
            
            is_reading, _ = camera.read()            
            if is_reading:
                cams.append(camera)
                cams_ids.append(camera_idx)
                
            camera_idx +=1

        return cams, cams_ids
    
    def play(self):
        self.player.play()    
        self.audio_icon.setPixmap(QPixmap.fromImage(QImage(os.path.join('GUI', 'icons', 'speaker.png'))).scaledToHeight(self.audio_button.geometry().height()))