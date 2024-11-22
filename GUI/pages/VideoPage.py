from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

class VideoPage(QWidget):
    
    videoStarted = pyqtSignal()
    videoEnded = pyqtSignal(int)
    
    def __init__(self, parent, video_path:str, participant_id:int):
        super().__init__()
        self.parent_window = parent
        self.video_path = video_path
        self.participant_id = participant_id
        
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
        
    def statusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.video.hide()
            self.player.stop()
            self.parent_window.next_page()
            self.videoEnded.emit(self.participant_id)

    def showEvent(self, QShowEvent):
        self.player.play()
        self.video.show()
        self.videoStarted.emit()