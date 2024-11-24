from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import os
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer

class WebcamPreviewWindow(QDialog):
    
    okClicked = pyqtSignal()
    
    def __init__(self, parent, cap):
        super().__init__()
                
        self.parent_window = parent

        self.cap = cap
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        self.setupUi()
        self.ok_button.clicked.connect(self.ok_button_clicked)
        self.setContentsMargins(20,20,20,20)
        self.setWindowTitle("Calibrazione Webcam")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons','webcam.png')))
        
        self.update_frame()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1e3/self.fps))
        
    # Generated with QtDesigner
    def setupUi(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QLabel(self)
        self.label_2.setStyleSheet("font: 20pt \"Rubik Light\";\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, Qt.AlignHCenter)
        self.label = QLabel(self)
        self.label.setStyleSheet("font:12pt \"Rubik Light\";\n"
"color: rgb(10,10,10);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignHCenter)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.video_label = QLabel(self)
        self.video_label.setText("")
        self.video_label.setObjectName("video_label")
        self.verticalLayout_2.addWidget(self.video_label, 0, Qt.AlignHCenter)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.label_3 = QLabel(self)
        self.label_3.setStyleSheet("font:10pt \"Rubik Light\";\n"
"color: rgb(255, 0, 0);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3, 0, Qt.AlignHCenter)
        self.ok_button = QPushButton(self)
        self.ok_button.setMinimumSize(QSize(150, 50))
        self.ok_button.setMaximumSize(QSize(150, 16777215))
        self.ok_button.setStyleSheet("border-radius: 15px;\n"
"font: 15pt \"Rubik Light\";\n"
"color: rgb(255,255,255);\n"
"background-color: rgb(0, 64, 130);")
        self.ok_button.setObjectName("ok_button")
        self.verticalLayout_2.addWidget(self.ok_button, 0, Qt.AlignHCenter)
        
        self.label_2.setText("Benvenuto!")
        self.label.setText("Prima di iniziare, controlla l'inquadratura della webcam")
        self.label_3.setText("Assicurati di essere in un ambiente tranquillo e ben illuminato.")
        self.ok_button.setText("Ok")
            
    def ok_button_clicked(self):
        self.timer.stop()
        self.okClicked.emit()
        self.close()
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            overlay = cv2.imread(os.path.join('GUI', 'icons', 'sagoma.png'), cv2.IMREAD_UNCHANGED)            
            overlay = cv2.resize(overlay, (frame.shape[1], frame.shape[0]))

            alpha = overlay[:,:,3]
            alpha = cv2.merge([alpha,alpha,alpha])
            front = overlay[:,:,0:3]
            result = np.where(alpha==(0,0,0), frame, front)
                
            rgb_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))