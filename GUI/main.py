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
import tempfile
import shutil

class MainWindow(QMainWindow):
    
    def __init__(self, app, rest_time=5, protocol_file_path=None):
        super().__init__()
    
        self.app = app
        self.rest_time = rest_time
        self.protocol_file_path = protocol_file_path
        self.webcamRecorder = None
        self.subject = None
        self.temp_dir = None
        
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Interfaccia")
        self.resize(QApplication.desktop().availableGeometry(0).size())
        
        self.setStyleSheet("background-color: white;") 
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.load_resources()
        
    def load_resources(self):
 
        try:
            df = pd.read_csv(self.protocol_file_path, sep=',')
        except:
            self.add_page(TextPage(self, "File protocollo non trovato!", "Assicuratevi che il file sia nominato correttamente.\nExpected name: protocol.csv", "Esci", self.close))
            return
        
        subject_id = 0
        subject_ids = os.listdir(Subject.data_dir)
        if len(subject_ids) != 0:
            subject_ids.sort()
            subject_id = int(subject_ids.pop()) + 1
        self.subject = Subject(subject_id)
        self.protocol = df[df['SubjectID'] == subject_id].squeeze()
        
        if self.protocol.empty:
            self.add_page(TextPage(self, "The End?", "Non ho trovato una riga valida nel file di protocollo.\nAssicuratevi che il file di protocollo sia aggiornato e non ci siano linee mancanti.", "Esci", button_slot=self.close))
            return
        
        self.temp_dir = tempfile.mkdtemp()
        
        try:
            self.webcamRecorder = WebcamRecorder(output_file=os.path.join(self.temp_dir, "recording.mp4"), daemon=True)
        except:
            self.add_page(TextPage(self, "Nessuna webcam valida trovata!", "Assicuratevi che un dispositivo webcam sia collegato e funzioni correttamente.", "Esci", button_slot=self.close))
            return
    
        self.video_descriptor1 = VideoDescriptor(self.protocol.video_path1)
        self.video_descriptor2 = VideoDescriptor(self.protocol.video_path2)
        
        if self.video_descriptor1.type == self.video_descriptor2.type:
            self.add_page(TextPage(self, "Errore nel file di protocollo!", "C'è qualcosa che non va nei video selezionati. Controllare il file di protocollo.", "Esci", button_slot=self.close))
            return
    
        self.setup_pages()
    
    def setup_pages(self):
        
        self.add_page(TextPage(self, "Benvenuto!", "Oggi parteciperai a un'esperienza.\nPer prima cosa dovrai inserire alcuni tuoi dati.\nPremi Inizia quando sei pronto.", "Inizia"))
        self.add_page(DataCollectionPage(self))
        self.add_page(TextPage(self, "Bene!", "Ora ti mostreremo due video, su cui ti verranno fatte alcune domande.\nQuando sei pronto, premi Avanti, e inizierà il primo video.", "Avanti"))
        
        self.add_page(VideoPage(self, self.video_descriptor1.video_path))
        self.add_page(TextPage(self, "Question Time!", "Quando sei pronto, premi Avanti per iniziare il questionario associato al video che hai appena visto.", "Avanti"))
        self.add_page(Poll(self, self.video_descriptor1.getQuestions()))
        self.add_page(RestPage(self, "Ci Prendiamo una piccola pausa!\nA breve ti mostreremo il prossimo video.", self.rest_time))
        
        self.add_page(VideoPage(self, self.video_descriptor2.video_path))
        self.add_page(TextPage(self, "Quasi Fatto!", "Quando sei pronto, premi Avanti per iniziare il questionario associato al video che hai appena visto.", "Avanti"))
        self.add_page(Poll(self, self.video_descriptor2.getQuestions()))
            
        self.add_page(TextPage(self, "Grazie mille!", "La nostra esperienza si è conclusa, grazie mille per la partecipazione.\nPremi Fine per uscire.", "Fine", button_slot=self.save_and_close))
        
    def add_page(self, page):
        self.stacked_widget.addWidget(page)
    
    def next_page(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
    
    def showEvent(self, QShowEvent):
        if self.webcamRecorder is not None:
            self.webcamRecorder.start()
        if self.subject is not None:
            self.subject.set_session_start_timestamp()
            
    def closeEvent(self, QCloseEvent):
        if self.webcamRecorder is not None:
            self.webcamRecorder.stop()
        if self.temp_dir is not None:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def save_and_close(self):
        if self.webcamRecorder is not None:
            self.webcamRecorder.stop()
        if self.subject is not None:
            self.subject.set_session_end_timestamp()
            self.subject.dump_to_file(self.temp_dir)
            shutil.copytree(self.temp_dir, self.subject.subject_dir(), dirs_exist_ok=True)
        self.close()
    
def run_main():
    if sys.platform == 'win32':
        os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
        
    app = QApplication(sys.argv)
    opening_msg = QMessageBox()
    opening_msg.setWindowTitle("Interfaccia")
    opening_msg.setText("Stiamo caricando tutte le risorse necessarie...\t")
    opening_msg.setStandardButtons(QMessageBox.NoButton)
    opening_msg.show()
    window = MainWindow(app, rest_time=1, protocol_file_path="protocol.csv")
    window.showFullScreen()
    opening_msg.reject()
    sys.exit(app.exec_())