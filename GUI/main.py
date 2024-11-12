from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.pages.TextPage import *
from GUI.pages.IntroPage import *
from GUI.pages.DataCollectionPage import *
from GUI.pages.QuestionScalePage import *
from GUI.pages.CountDownPage import *
from GUI.pages.VideoPage import *
from GUI.pages.PANAS import *
from GUI.pages.WebcamPreviewWindow import *
from GUI.pages.WebcamSelectionWindow import *

from backend.config import load_config
from backend.WebcamRecorder import *
from backend.ScreenRecorder import *
from backend.VideoDescriptor import *
from backend.Participant import *
from backend.eye_tracking.EyeTracker import *

import sys
import os
import tempfile
import shutil

class MainWindow(QMainWindow):
    
    def __init__(self, app, config_file='config.json'):
        super().__init__()
    
        self.app = app
        self.webcamRecorder = None
        self.screenRecorder = None
        self.eyeTracker = None
        self.participant = None
        self.temp_dir = None
        self.cap = None
        
        self.webcam_selection_window = WebcamSelectionWindow(app)
        self.webcam_selection_window.capSelected.connect(self.show_webcam_preview_window)

        config = load_config(config_file)
        
        self.VIDEO_FOLDER = config['app']['VIDEO_FOLDER']
        self.DATA_FOLDER = config['app']['DATA_FOLDER']
        self.PANAS_SCALE = config['app']['QUESTIONS']['PANAS']['SCALE']
        self.PANAS_EMOTIONS = config['app']['QUESTIONS']['PANAS']['EMOTIONS']
        self.PANAS_POSITIVE = config['app']['QUESTIONS']['PANAS']['POSITIVE']
        self.PANAS_NEGATIVE = config['app']['QUESTIONS']['PANAS']['NEGATIVE']
        self.QUESTIONS_BEFORE = config['app']['QUESTIONS']['BEFORE']
        self.QUESTIONS_AFTER = config['app']['QUESTIONS']['AFTER']
            
        self.setup_eye_tracker()
             
    def launch(self):
        self.setupUI()        
        self.load_resources()
        self.setup_pages()
        self.showFullScreen()

    def show_webcam_preview_window(self, cap):
        self.cap = cap
        self.webcam_preview_window = WebcamPreviewWindow(self, self.cap)
        self.webcam_preview_window.okClicked.connect(self.launch)        
        self.webcam_preview_window.show()

    def setupUI(self):
        self.setWindowTitle("Interfaccia")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
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
        
        self.video = videos[self.index % len(videos)]
        self.index = (self.index + 1) % len(videos)
        
        if self.cap is None:
            raise RuntimeError("Cap not initialized")
        
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.webcamRecorder = WebcamRecorder(output_file=os.path.join(self.temp_dir, "webcam.mp4"), daemon=True, cap=self.cap)
        except Exception as e:
            self.add_page(TextPage(self, str(e), "Assicuratevi che un dispositivo webcam sia collegato e funzioni correttamente.", "Esci", button_slot=self.close))
            return
        
        participant_id = 0
        participant_ids = os.listdir(self.DATA_FOLDER)
        if len(participant_ids) != 0:
            participant_ids.sort()
            participant_id = int(participant_ids.pop()) + 1
        self.participant = Participant(participant_id, self.DATA_FOLDER)
        
        screen_size = self.app.primaryScreen().size()
        self.screenRecorder = ScreenRecorder(output_file=os.path.join(self.temp_dir, "screen.mp4"), fps=24.0, resolution=(screen_size.width(), screen_size.height()), daemon=True)
        
    def setup_eye_tracker(self):
        try:
            self.eyeTracker = EyeTracker(self.temp_dir)
        except:
            print("No eye-tracker found. Starting without eye-tracker..")

        if self.eyeTracker:
            self.eyeTracker.setup_tracking()
            
    def setup_pages(self):
        
        intro_page = self.add_page(IntroPage(self, "Benvenuto!", "Grazie per aver accettato di partecipare a questo studio.\nDurante la sessione, ti sarà richiesto di guardare una breve videolezione di circa 5-10 minuti su un tema didattico. Mentre guardi il video, alcuni dispositivi registreranno automaticamente i tuoi movimenti oculari e il tuo battito cardiaco, e sarà inoltre monitorata l’espressione facciale per analizzare le reazioni emotive.\n\nDopo la visione, ti chiederemo di completare alcuni questionari. L’intera sessione durerà circa 15-20 minuti. Ti invitiamo a seguire il video con attenzione e a rispondere ai questionari finali.\n", "Inizia", warning_text="Siediti comodamente, ma cerca di non muovere la mano dove indossi l'orologio, interagendo con questa interfaccia solo con la mano libera, facendo uso del mouse. Evita di coprire il volto con la mano e leggi a mente.", bottom_text="I dati raccolti saranno utilizzati esclusivamente per scopi di ricerca, e tutte le informazioni rimarranno anonime.\nSe in qualsiasi momento desideri interrompere l’esperimento, sei libero di farlo. Buona visione e grazie per il tuo tempo!", error_text="Per favore fornisci il tuo consenso per iniziare lo studio"))
        intro_page.readyClicked.connect(self.start_capture)
        intro_page.exitClicked.connect(self.close)
        
        self.add_page(DataCollectionPage(self))
        panas_page_before = self.add_page(PANAS(self, emotions=self.PANAS_EMOTIONS, scale=self.PANAS_SCALE, positive=self.PANAS_POSITIVE, negative=self.PANAS_NEGATIVE, flag="PRIMA"))
        panas_page_before.nextClicked.connect(self.participant.add_answers)
        for question in self.QUESTIONS_BEFORE:
            self.add_page(QuestionScalePage(self, "Questionario Preparatorio", question))
        self.add_page(TextPage(self, "È tutto pronto!", "Quando sei pronto, premi Avanti per iniziare. Il video inizierà a seguito di un breve conto alla rovescia.", "Avanti"))
        
        real = random.choice([True, False])
        
        self.add_page(CountDownPage(self, seconds=3))     
        self.add_page(VideoPage(self, self.video.getRandomVideo(real=real), video_type='real' if real else 'fake'))
        self.add_page(TextPage(self, "Question Time!", "Quando sei pronto, premi Avanti per iniziare il questionario.", "Avanti"))
        panas_page_after = self.add_page(PANAS(self, emotions=self.PANAS_EMOTIONS, scale=self.PANAS_SCALE, positive=self.PANAS_POSITIVE, negative=self.PANAS_NEGATIVE, flag="DOPO"))
        panas_page_after.nextClicked.connect(self.participant.add_answers)
        for i, question in enumerate(self.QUESTIONS_AFTER):
            self.add_page(QuestionScalePage(self, "Domanda " + str(i+1), question))
  
        self.add_page(TextPage(self, "Fine!", "Il nostro esperimento si è concluso, grazie mille per la partecipazione.\nPremi Fine per uscire.", "Fine", button_slot=self.save_and_close))
        
    def add_page(self, page):
        self.stacked_widget.addWidget(page)
        return page
    
    def next_page(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
    
    def start_capture(self):
        if self.eyeTracker is not None:
            self.eyeTracker.start_recording(self.participant.id)
        if self.webcamRecorder is not None:
            self.webcamRecorder.start()
        if self.screenRecorder is not None:
            self.screenRecorder.start()
        if self.participant is not None:
            self.participant.set_session_start_timestamp()
            
    def stop_capture(self):
        if self.webcamRecorder is not None and self.webcamRecorder.recording:
            self.webcamRecorder.stop()
        if self.eyeTracker is not None:
            try:
                self.eyeTracker.stop_recording()
            except:
                pass
        if self.screenRecorder is not None and self.screenRecorder.recording:
            self.screenRecorder.stop()
            
    def closeEvent(self, QCloseEvent):
        self.stop_capture()
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
                
        if self.participant is not None:
            self.participant.set_session_end_timestamp()
            self.participant.dump_to_file(self.temp_dir)
        
        self.stop_capture()
        
        shutil.copytree(self.temp_dir, self.participant.participant_dir(), dirs_exist_ok=True)
        
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
    window = MainWindow(app)
    window.webcam_selection_window.show()
    opening_msg.reject()
    sys.exit(app.exec_())