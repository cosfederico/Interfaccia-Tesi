from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.pages.TextPage import *
from GUI.pages.DataCollectionPage import *
from GUI.pages.CountDownPage import *
from GUI.pages.VideoPage import *

from backend.config import load_config
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
    
    def __init__(self, app, config_file='config.json'):
        super().__init__()
    
        self.app = app
        self.webcamRecorder = None
        self.subject = None
        self.temp_dir = None
        

        config = load_config(config_file)
        
        self.VIDEO_FOLDER = config['app']['VIDEO_FOLDER']
        self.DATA_FOLDER = config['app']['DATA_FOLDER']
                
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Interfaccia")
        self.resize(QApplication.desktop().availableGeometry(0).size())
        
        self.setStyleSheet("background-color: white;") 
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.load_resources()
        
    def load_resources(self):
        
        self.index = None
        try:
            with open(os.path.join(self.VIDEO_FOLDER, 'index'), 'r') as f:
                self.index = int(f.readline())
        except:
            self.add_page(TextPage(self, "Errore", "Il file di indice dei video è invalido o inesistente.", "Esci", button_slot=self.close))
            return
        
        try:
            videos = [VideoDescriptor(os.path.join(self.VIDEO_FOLDER, video)) for video in next(os.walk(self.VIDEO_FOLDER))[1]]
        except Exception as e:
            self.add_page(TextPage(self, "Errore nel caricamento video", str(e), "Esci", button_slot=self.close))
            return
        
        if len(videos) == 0:
            self.add_page(TextPage(self, "Cartella video vuota", "Nessun video da riprodurre trovato.\nPer favore carica dei video da riprodurre e riavvia il programma.", "Esci", self.close))
            return
        
        self.video1 = videos[self.index % len(videos)]
        self.video2 = videos[(self.index + 1) % len(videos)]
        self.index = (self.index + 2) % len(videos)
        
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.webcamRecorder = WebcamRecorder(output_file=os.path.join(self.temp_dir, "recording.mp4"), daemon=True)
        except Exception as e:
            self.add_page(TextPage(self, str(e), "Assicuratevi che un dispositivo webcam sia collegato e funzioni correttamente.", "Esci", button_slot=self.close))
            return
        
        subject_id = 0
        subject_ids = os.listdir(self.DATA_FOLDER)
        if len(subject_ids) != 0:
            subject_ids.sort()
            subject_id = int(subject_ids.pop()) + 1
        self.subject = Subject(subject_id, self.DATA_FOLDER)
    
        self.setup_pages()
    
    def setup_pages(self):
        
        self.add_page(TextPage(self, "Benvenuto!", "Oggi parteciperai a un'esperienza.\nPer prima cosa dovrai inserire alcuni tuoi dati.\nPremi Inizia quando sei pronto.", "Inizia"))
        self.add_page(DataCollectionPage(self))
        self.add_page(TextPage(self, "Bene!", "Ora ti mostreremo due video, su cui ti verranno fatte alcune domande.\nQuando sei pronto, premi Avanti, e inizierà il primo video.", "Avanti"))
        
        real = random.choice([True, False])
        
        self.add_page(CountDownPage(self, seconds=3))     
        self.add_page(VideoPage(self, self.video1.getRandomVideo(real=real)))
        self.add_page(TextPage(self, "Question Time!", "Quando sei pronto, premi Avanti per iniziare il questionario associato al video che hai appena visto.", "Avanti"))
        self.add_page(Poll(self, self.video1.getQuestions()))
        
        self.add_page(TextPage(self, "Grazie mille delle risposte","Puoi fare una breve pausa.\nQuando sei pronto premi Avanti per iniziare il prossimo video.", "Avanti"))
  
        self.add_page(CountDownPage(self, seconds=3)) 
        self.add_page(VideoPage(self, self.video2.getRandomVideo(real=not real)))
        self.add_page(TextPage(self, "Question Time!", "Quando sei pronto, premi Avanti per iniziare il questionario associato al video che hai appena visto.", "Avanti"))
        self.add_page(Poll(self, self.video2.getQuestions()))
           
        self.add_page(TextPage(self, "Fine!", "La nostra esperienza si è conclusa, grazie mille per la partecipazione.\nPremi Fine per uscire.", "Fine", button_slot=self.save_and_close))
        
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
        if self.webcamRecorder is not None and self.webcamRecorder.recording:
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
        try:
            with open(os.path.join(self.VIDEO_FOLDER, 'index'), 'w') as f:
                f.write(str(self.index))
        except:
            pass
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
    window = MainWindow(app)
    window.showFullScreen()
    opening_msg.reject()
    sys.exit(app.exec_())