from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.pages.TextPage import *
from GUI.pages.DataCollectionPage import *
from GUI.pages.CountDownPage import *
from GUI.pages.VideoPage import *
from GUI.pages.WebcamPopup import *

from backend.config import load_config
from backend.Poll import *
from backend.WebcamRecorder import *
from backend.ScreenRecorder import *
from backend.VideoDescriptor import *
from backend.Subject import *
from backend.eye_tracking.EyeTracker import *

import sys
import os
import tempfile
import shutil

class MainWindow(QMainWindow):
    
    def __init__(self, app, cap=None, config_file='config.json'):
        super().__init__()
    
        self.app = app
        self.webcamRecorder = None
        self.screenRecorder = None
        self.eyeTracker = None
        self.subject = None
        self.temp_dir = None
        self.cap = cap

        config = load_config(config_file)
        
        self.VIDEO_FOLDER = config['app']['VIDEO_FOLDER']
        self.DATA_FOLDER = config['app']['DATA_FOLDER']
                
        self.setupUI()
        self.load_resources()
        self.setup_pages()

    def setupUI(self):
        self.setWindowTitle("Interfaccia")
        self.resize(QApplication.desktop().availableGeometry(0).size())
        
        self.setStyleSheet("background-color: white;") 
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
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
            self.webcamRecorder = WebcamRecorder(output_file=os.path.join(self.temp_dir, "recording.mp4"), daemon=True, cap=self.cap)
        except Exception as e:
            self.add_page(TextPage(self, str(e), "Assicuratevi che un dispositivo webcam sia collegato e funzioni correttamente.", "Esci", button_slot=self.close))
            return
        
        subject_id = 0
        subject_ids = os.listdir(self.DATA_FOLDER)
        if len(subject_ids) != 0:
            subject_ids.sort()
            subject_id = int(subject_ids.pop()) + 1
        self.subject = Subject(subject_id, self.DATA_FOLDER)
        
        screen_size = self.app.primaryScreen().size()
        self.screenRecorder = ScreenRecorder(output_file=os.path.join(self.temp_dir, "screen.mp4"), fps=24.0, resolution=(screen_size.width(), screen_size.height()), daemon=True)
        
        try:
            self.eyeTracker = EyeTracker(self.temp_dir, 'test')
        except:
            print("No eye-tracker found. Starting without eye-tracker..")

        if self.eyeTracker:
            self.eyeTracker.setup_tracking()
            
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
        if self.screenRecorder is not None:
            self.screenRecorder.start()
        if self.subject is not None:
            self.subject.set_session_start_timestamp()
        if self.eyeTracker is not None:
            self.eyeTracker.start_recording(self.subject.id)
            
    def release_resources(self):
        if self.screenRecorder is not None and self.screenRecorder.recording:
            self.screenRecorder.stop()
        if self.webcamRecorder is not None and self.webcamRecorder.recording:
            self.webcamRecorder.stop()
        if self.eyeTracker is not None:
            try:
                self.eyeTracker.stop_recording()
            except:
                pass
            
    def closeEvent(self, QCloseEvent):
        self.release_resources()
        if self.temp_dir is not None:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def save_and_close(self):
        self.hide()
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Interfaccia")
        msg.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
        msg.setText("Salvataggio dei dati raccolti...\t")
        msg.setStandardButtons(QMessageBox.NoButton)
        msg.show()
        self.app.processEvents()
                
        if self.subject is not None:
            self.subject.set_session_end_timestamp()
            self.subject.dump_to_file(self.temp_dir)
        
        self.release_resources()
        
        shutil.copytree(self.temp_dir, self.subject.subject_dir(), dirs_exist_ok=True)
        
        try:
            with open(os.path.join(self.VIDEO_FOLDER, 'index'), 'w') as f:
                f.write(str(self.index))
        except:
            pass
        
        msg.close()
        self.close()
        
def run_main():
    if sys.platform == 'win32':
        os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
        
    app = QApplication(sys.argv)
    
    opening_msg = QMessageBox()
    opening_msg.setWindowTitle("Interfaccia")
    opening_msg.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
    opening_msg.setText("Stiamo caricando le risorse necessarie...\t")
    opening_msg.setStandardButtons(QMessageBox.NoButton)
    opening_msg.show()
    
    cap = cv2.VideoCapture(0)
    opening_msg.reject()
  
    if cap is None or not cap.isOpened():
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
        error_msg.setWindowTitle("Webcam Unavailable")
        error_msg.setText("Impossibile avviare la webcam.\nAssicurati che sia connessa correttamente e non sia in uso da un altro programma.")
        error_msg.exec_()
        sys.exit()
        
    window = MainWindow(app, cap)
    webcam_window = WebcamPopup(app, cap, action=window.showFullScreen)
    webcam_window.show()
    sys.exit(app.exec_())