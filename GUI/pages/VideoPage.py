from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

from backend.Poll import *

class CustomVideoWidget(QVideoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if self.parent:
            self.parent.keyPressEvent(event)
        else:
            super().keyPressEvent(event)
            
    def mouseDoubleClickEvent(self, event):
        if self.parent:
            self.parent.mouseDoubleClickEvent(event)
        else:
            super().mouseDoubleClickEvent(event)

class VideoPage(QWidget):
    
    def __init__(self, parent, video_path):
        super().__init__()
        self.parent_window = parent
        self.video_path = video_path
        
        self.video = CustomVideoWidget(self)
        self.video.resize(self.parent_window.size())
        
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
      
        self.player.mediaStatusChanged.connect(self.statusChanged)
     
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            event.accept()
        elif event.key() == Qt.Key_Space and self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            event.accept()            
        else:
            super(VideoPage, self).keyPressEvent(event)
 
    def load_video(self):
        self.player.setMedia(QMediaContent(QUrl(self.video_path)))
 
    def play(self):
        self.load_video()
        self.player.setPosition(0)
        self.video.show()
        self.player.play()
        
    def statusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.stop()
            self.video_ended()
                    
    def video_ended(self):
        self.parent_window.next_page()
        
    def showEvent(self, QShowEvent):
        self.play()
        self.parent_window.subject.add_video_timestamp(self.video_path)