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
        
        loadUi("GUI/qtdesigner/WebcamPreviewWindow.ui", self)
        self.ok_button.clicked.connect(self.ok_button_clicked)
        self.setContentsMargins(20,20,20,20)
        self.setWindowTitle("Calibrazione Webcam")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons','webcam.png')))
        
        self.update_frame()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1e3/self.fps))
            
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