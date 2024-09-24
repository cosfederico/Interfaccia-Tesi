from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

class VideoPage(QWidget):
    
    def __init__(self, parent, video_path):
        super().__init__()
        self.parent_window = parent
        self.video_path = video_path
        
        self.video = QVideoWidget(self)
        self.video.resize(self.parent_window.frameSize())
        
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
        
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
    
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
 
    def play(self):
        self.player.setPosition(0)
        self.video.show()
        self.player.play()
        
    def statusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.stop()
            self.video_ended()
                    
    def video_ended(self):
        self.parent_window.subject.add_video_end_timestamp()
        self.parent_window.next_page()
        
    def showEvent(self, QShowEvent):
        self.play()
        self.parent_window.subject.add_video_start_timestamp(self.video_path)