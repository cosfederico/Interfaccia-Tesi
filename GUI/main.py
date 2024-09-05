from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.pages.TextPage import *
from GUI.pages.RestPage import *
from GUI.pages.DataCollectionPage import *
from GUI.pages.VideoPage import *

from backend.Poll import *
from backend.WebcamRecorder import *
from backend.VideoDescriptor import *
from backend.Subject import *

import pandas as pd
import sys
import os

class MainWindow(QMainWindow):
    
    def __init__(self, app, rest_time=5, protocol_file_path=None):
        super().__init__()
    
        self.app = app
        self.rest_time = rest_time
        self.webcamRecorder = None
        
        subject_id = 0
        subject_ids = os.listdir(Subject.data_dir)
        if len(subject_ids) != 0:
            subject_ids.sort()
            subject_id = int(subject_ids.pop()) + 1
        
        self.subject = Subject(subject_id)
                
        try:
            df = pd.read_csv(protocol_file_path, sep=',')
        except:
            self.protocol = None
        else:
            self.protocol = df[df['SubjectID'] == subject_id].squeeze()
            if not self.protocol.empty and not os.path.isdir(self.subject.subject_dir()):
                os.mkdir(self.subject.subject_dir())
            self.webcamRecorder = WebcamRecorder(output_file=self.subject.subject_dir() + "/recording.mp4", daemon=True)

        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("Interfaccia")
        self.resize(QApplication.desktop().availableGeometry(0).size())
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        if self.webcamRecorder.cap is None or not self.webcamRecorder.cap.isOpened():
            self.add_page(TextPage(self, "Nessuna webcam valida trovata!", "Assicuratevi che un dispositivo webcam sia collegato e funzioni correttamente.", "Esci"))
            return
        elif self.protocol is None:
            self.add_page(TextPage(self, "Errore!", "File protocollo non trovato. Assicuratevi che il file sia nominato correttamente.\nExpected name: protocol.csv", "Esci"))
            return
        elif self.protocol.empty:
            self.add_page(TextPage(self, "Errore!", "Non ho trovato una riga valida nel file di protocollo.\nAssicuratevi che il file di protocollo sia aggiornato e non ci siano linee mancanti.", "Esci"))
            return
        
        self.add_page(TextPage(self, "Benvenuto!", "Oggi parteciperai a un'esperienza.\nPer prima cosa dovrai inserire alcuni tuoi dati.\nPremi Inizia quando sei pronto.", "Inizia"))
        self.add_page(DataCollectionPage(self))
        self.add_page(TextPage(self, "Bene!", "Ora ti mostreremo due video, su cui ti verranno fatte alcune domande.\nQuando se pronto, premi Avanti, e inizierà il primo video.", "Avanti"))
        
        self.load_videos()
        
    def load_videos(self):
        
        video_descriptor1 = VideoDescriptor(self.protocol.video1)
        video_descriptor2 = VideoDescriptor(self.protocol.video2)
   
        self.add_page(VideoPage(self, video_descriptor1.getReal()))
        self.add_page(Poll(self, video_descriptor1.getQuestions()))
        self.add_page(RestPage(self, "attendi", self.rest_time))
        
        self.add_page(VideoPage(self, video_descriptor2.getRandomFake()))
        self.add_page(Poll(self, video_descriptor2.getQuestions()))
        self.add_page(RestPage(self, "attendi", self.rest_time))
            
        self.add_page(TextPage(self, "La nostra esperienza si è conclusa!", "Grazie mille per la partecipazione.", "Fine"))
        
    def add_page(self, page):
        self.stacked_widget.addWidget(page)
 
    def insert_page(self, page):
        self.stacked_widget.insertWidget(self.stacked_widget.currentIndex()+1, page)
    
    def next_page(self):
        if (self.stacked_widget.currentIndex() + 1 >= self.stacked_widget.count()):
            self.quit()
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
    
    def showEvent(self, QShowEvent):
        if self.webcamRecorder is not None:
            self.webcamRecorder.start()
        self.subject.set_session_start_timestamp()
    
    def quit(self):
        if self.webcamRecorder is not None:
            self.webcamRecorder.stop()
        self.subject.set_session_end_timestamp()
        if not (self.webcamRecorder.cap is None or not self.webcamRecorder.cap.isOpened() or self.protocol is None or self.protocol.empty):
            self.subject.dump_to_file("")
        self.close()
    
def run_main():
    app = QApplication(sys.argv)
    opening_msg = QMessageBox()
    opening_msg.setWindowTitle("Interfaccia")
    opening_msg.setText("Stiamo caricando tutte le risorse necessarie...\t")
    opening_msg.setStandardButtons(QMessageBox.NoButton)
    opening_msg.show()
    window = MainWindow(app, rest_time=1, protocol_file_path="protocol.csv")
    opening_msg.reject()
    window.showFullScreen()
    sys.exit(app.exec_())