from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from GUI.pages.WebcamPreviewWindow import *

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
        box_layout.addWidget(QLabel("Webcam %d (%d x %d)" %(self.id+1, self.frame_width, self.frame_height)), alignment=Qt.AlignCenter)
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
    
    capSelected = pyqtSignal(cv2.VideoCapture)
        
    def __init__(self, app, text="Prima di iniziare, scegli la webcam da utilizzare"):
        super().__init__()
        
        self.app = app
        self.text_str = text
        self.boxes = []
        self.selected_box = None
                        
        self.setupUI()
                
    def setupUI(self):
        loadUi("GUI/qtdesigner/WebcamSelectionWindow.ui",self)
        self.setContentsMargins(100,100,100,100)
        self.setWindowTitle("Selezione Webcam")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons','webcam.png')))
                
        self.text.setText(self.text_str)
        self.done_button.clicked.connect(self.done_button_clicked)
        
        self.load_cams()
        
    def load_cams(self):
        
        cams = self.get_working_webcams()
        
        if len(cams) == 0:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
            error_msg.setWindowTitle("Interfaccia")
            error_msg.setText("Nessuna webcam disponibile trovata.\nAssicurati di avere almeno una webcam collegata al computer, non in uso da un altro programma.")
            error_msg.exec_()
            sys.exit()
            
        videos_layout = QGridLayout()
        
        for i, cam in enumerate(cams):
            box = CameraBox(cam, id=i)
            box.selected.connect(self.box_selected)   
            box.deselected.connect(self.box_deselected)   
            self.boxes.append(box)
            videos_layout.addWidget(box, i/3, i%3, alignment=Qt.AlignTop)
        
        self.box.setLayout(videos_layout)
        
    def box_selected(self, selected_box):
        for box in self.boxes:
            if box.isSelected:
                box.select(False)
        self.selected_box = selected_box
        
    def box_deselected(self):
        self.selected_box = None
        
    def done_button_clicked(self):
        
        if not self.selected_box:
            return
        
        for box in self.boxes:
            if box != self.selected_box:
                box.release_resources()
        
        self.capSelected.emit(self.selected_box.cap)
        self.close()
        
    def get_working_webcams(self):

        camera_idx = 0
        cams = []
        
        while True:
            camera = cv2.VideoCapture(camera_idx)
            if not camera.isOpened():
                break
            
            is_reading, _ = camera.read()            
            if is_reading:
                cams.append(camera)
                
            camera_idx +=1

        return cams