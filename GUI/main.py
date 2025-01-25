from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.pages.TextPage import *
from GUI.pages.IntroPage import *
from GUI.pages.DataCollectionPage import *
from GUI.pages.QuestionScalePage import *
from GUI.pages.MultipleChoiceQuestionPage import *
from GUI.pages.CountDownPage import *
from GUI.pages.VideoPage import *
from GUI.pages.PANAS import *

from GUI.windows.WebcamPreviewWindow import *
from GUI.windows.WebcamSelectionWindow import *
from GUI.windows.LoadingPopup import *

from backend.config import load_config
from backend.WebcamRecorder import *
from backend.ScreenRecorder import *
from backend.VideosManager import *
from backend.Participant import *
from backend.eye_tracking.EyeTracker import *

import sys
import os
import tempfile
import shutil

class MainWindow(QMainWindow):
    
    def __init__(self, app:QApplication, config_file='config.json'):
        super().__init__()
    
        self.app = app
        self.config_file = config_file
        self.webcamRecorder = None
        self.screenRecorder = None
        self.videosManager = None
        self.eyeTracker = None
        self.participant = None
        self.temp_dir = None
        self.cap = None
        
        self.webcam_selection_window = WebcamSelectionWindow(app)
        self.webcam_selection_window.capSelected.connect(self.show_webcam_preview_window)

        config = load_config(self.config_file)
        
        self.VIDEO_FOLDER = config['app']['VIDEO_FOLDER']
        self.DATA_FOLDER = config['app']['DATA_FOLDER']
        self.PANAS_SCALE = config['app']['QUESTIONS']['PANAS']['SCALE']
        self.PANAS_EMOTIONS = config['app']['QUESTIONS']['PANAS']['EMOTIONS']
        self.PANAS_POSITIVE = config['app']['QUESTIONS']['PANAS']['POSITIVE']
        self.PANAS_NEGATIVE = config['app']['QUESTIONS']['PANAS']['NEGATIVE']
        self.QUESTIONS_BEFORE = config['app']['QUESTIONS']['BEFORE']
        self.QUESTIONS_AFTER = config['app']['QUESTIONS']['AFTER']
            
        self.temp_dir = tempfile.mkdtemp()
        self.setup_eye_tracker()
             
    def launch(self):
        self.webcam_preview_window.close() 
        loading_msg = LoadingPopup(self.app, "Caricamento...")
        self.setupUI()        
        self.load_resources()
        loading_msg.close()
        self.showFullScreen()

    def show_webcam_preview_window(self, cap, cap_id):
        self.cap = cap
        self.cap_id = cap_id
        self.webcam_preview_window = WebcamPreviewWindow(self, self.cap)
        self.webcam_preview_window.okClicked.connect(self.launch)        
        self.webcam_preview_window.show()

    def setupUI(self):
        self.setWindowTitle("Interfaccia")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons', 'webcam.png')))
        
        self.setStyleSheet("background-color: white;") 
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
    def load_resources(self):
        
        try:
            self.videosManager = VideosManager(videos_folder=self.VIDEO_FOLDER)
        except Exception as e:
            self.add_page(TextPage(self, "Benvenuto!", str(e) + "\nPuoi cambiare questo percorso nel file di configurazione " + self.config_file + ".", "Esci", button_slot=self.close))
            return
                
        if self.cap is None:
            self.add_page(TextPage(self, "Impossibile trovare la webcam", "Qualcosa è andato storto nel caricamento della webcam, assicurarsi non sia in uso da un altro programma e riavviare il programma.", "Esci", self.close))
            return
        
        try:
            self.webcamRecorder = WebcamRecorder(cap_id=self.cap_id, cap=self.cap, output_file=os.path.join(self.temp_dir, "webcam.mp4"))
        except Exception as e:
            self.add_page(TextPage(self, str(e), "Assicuratevi che un dispositivo webcam sia collegato e funzioni correttamente.", "Esci", button_slot=self.close))
            return
        
        participant_id = 0
        if not os.path.exists(self.DATA_FOLDER):
            os.mkdir(self.DATA_FOLDER)
        participant_ids = os.listdir(self.DATA_FOLDER)
        if len(participant_ids) != 0:
            participant_ids.sort()
            participant_id = int(participant_ids.pop()) + 1
        self.participant = Participant(participant_id, self.DATA_FOLDER)
                
        screen_size = self.app.primaryScreen().size()
        self.screenRecorder = ScreenRecorder(output_file=os.path.join(self.temp_dir, "screen.mp4"), fps=24.0, resolution=(screen_size.width(), screen_size.height()), daemon=True)
        
        self.setup_pages()
        
    def setup_eye_tracker(self):
        try:
            self.eyeTracker = EyeTracker(self.temp_dir)
        except:
            print("No eye-tracker found. Starting without eye-tracker..")

        if self.eyeTracker:
            self.eyeTracker.setup_tracking()
            
    def video_started(self):
        self.participant.set_video_start_timestamp()

    def video_ended(self, participant_id):
        self.participant.set_video_end_timestamp()
        features_names = self.videosManager.getFeaturesNames()
        features = self.videosManager.getVideoFeatures(participant_id)
        for name, feature in zip(features_names, features):
            self.participant.add_answer("Video " + name.title(), feature.title(), save_timestamp=False)
        self.participant.add_answer("Video File", self.videosManager.getVideoPath(participant_id), save_timestamp=False)    

    def setup_pages(self):
        
        intro_page = self.add_page(IntroPage(self, "Benvenuto!", "Grazie per aver accettato di partecipare a questo studio.\nDurante la sessione, ti sarà richiesto di guardare due brevi videolezioni di circa 5-10 minuti su un tema didattico. Mentre guardi i video, alcuni dispositivi registreranno automaticamente i tuoi movimenti oculari e il tuo battito cardiaco, e sarà inoltre monitorata l’espressione facciale per analizzare le reazioni emotive.\n\nDopo la visione, ti chiederemo di completare alcuni questionari. L’intera sessione durerà circa 20-30 minuti. Ti invitiamo a seguire i video con attenzione e a rispondere ai questionari finali.\n", "Inizia", warning_text="Siediti comodamente, ma cerca di non muovere la mano dove indossi l'orologio, interagendo con questa interfaccia solo con la mano libera, facendo uso del mouse. Evita di coprire il volto con la mano e leggi a mente.", bottom_text="I dati raccolti saranno utilizzati esclusivamente per scopi di ricerca, e tutte le informazioni rimarranno anonime.\nSe in qualsiasi momento desideri interrompere l’esperimento, sei libero di farlo. Buona visione e grazie per il tuo tempo!", error_text="Per favore fornisci il tuo consenso per iniziare lo studio"))
        intro_page.readyClicked.connect(self.start_capture)
        intro_page.exitClicked.connect(self.close)
        
        self.add_page(DataCollectionPage(self))
        
        panas_page_before = self.add_page(PANAS(self, emotions=self.PANAS_EMOTIONS, scale=self.PANAS_SCALE, positive=self.PANAS_POSITIVE, negative=self.PANAS_NEGATIVE, flag="PRIMA"))
        panas_page_before.nextClicked.connect(self.participant.add_answers)
        
        for question in self.QUESTIONS_BEFORE:
            self.add_page(QuestionScalePage(self, "Questionario Preparatorio", question))

        VES = [
            "Durante la visione ero pienamente concentrato sul video.",
            "Durante la visione era come se fossi presente solo a ciò che il video presentava.",
            "Quando stavo vedendo il video, i miei pensieri erano esclusivamente sul video.",
            "Dopo che il video si è concluso, ho avuto la sensazione di essere tornato nel 'mondo reale'.",
            "Dopo un po' di tempo che continuavo a vedere il video, mi è sembrato di diventare una cosa sola con la persona presente nel video.",
            "Mi sono immedesimato nella persona che parlava nel video.",
            "I contenuti del video sono stati coinvolgenti.",
            "Quando stavo vedendo il video, nella mia mente seguivo solo i suoi contenuti.",
            "Durante la visione del video, ho provato le stesse emozioni che provava la persona presente nel video.",
            "Ho trovato il video ingaggiante.",
            "Ho trovato interessante la persona presente nel video.",
            "Durante la visione del video, ero poco attento a cosa ci fosse o a cosa accadesse attorno a me.",
            "Ho avuto la sensazione pensare alle stesse cose che la persona presente nel video diceva.",
            "Nella mia immaginazione, era come se io fossi la persona che parlava nel video.",
            "Grazie al video, mi sono sentito soddisfatto."
        ]

        VES_intro = 'Indica quanto ti identifichi nelle seguenti affermazioni, in una scala da 1 a 7, dove 1 indica "Per niente", e 7 indica "Completamente".'
    
        for i, participant_id in enumerate([self.participant.id, ~self.participant.id]):

            if i == 0:
                self.add_page(TextPage(self, "Video " + str(i+1), "Quando sei pronto, premi Avanti per iniziare. Il video inizierà a seguito di un breve conto alla rovescia.", "Avanti"))
            else:
                self.add_page(TextPage(self, "Video " + str(i+1), "Quando sei pronto, premi Avanti per proseguire. Il prossima video inizierà a seguito di un breve conto alla rovescia.", "Avanti"))

            self.add_page(CountDownPage(self, seconds=3))
            video_page = self.add_page(VideoPage(self, self.videosManager.getVideoPath(participant_id), participant_id))
            video_page.videoStarted.connect(self.video_started)
            video_page.videoEnded.connect(self.video_ended)
        
            self.add_page(TextPage(self, "Question Time!", "Grazie mille per la visione. Ora ti invitiamo a rispondere a un paio di domande di valutazione sul video che hai appena visto.", "Inizia"))
            
            panas_page_after = self.add_page(PANAS(self, emotions=self.PANAS_EMOTIONS, scale=self.PANAS_SCALE, positive=self.PANAS_POSITIVE, negative=self.PANAS_NEGATIVE, flag="DOPO"))
            panas_page_after.nextClicked.connect(self.participant.add_answers)
        
            for i, question in enumerate(self.QUESTIONS_AFTER):
                self.add_page(QuestionScalePage(self, "Domanda di valutazione (" + str(i+1) + " di " + str(len(self.QUESTIONS_AFTER)) + ")", question))
  
            self.add_page(TextPage(self, "Bene!", "Ora passiamo ad alcune domande di comprensione a risposta multipla sulla lezione che hai appena visto.\nMi raccomando, scegli la risposta corretta!", "Inizia"))

            questions = self.videosManager.getVideoQuestions(participant_id)    
            for i, question in enumerate(questions):
                try:
                    right_answer = questions[question]["RIGHT_ANSWER"]
                    wrong_answers = questions[question]["WRONG_ANSWERS"]
                except KeyError as e:
                    print(e)
                    raise KeyError("Invalid questions.json for video " + video_page.video_path)
                question_page = self.add_page(MultipleChoiceQuestionPage(self, "Domanda di comprensione (" + str(i+1) + " di " + str(len(questions)) + ")", question, right_answer, wrong_answers))
                question_page.nextClicked.connect(self.participant.add_answers)

            self.add_page(QuestionScalePage(self, "Domanda di familiarità", "Quanto eri già familiare o a conoscenza dei contenuti mostrati nel video?"))
            self.add_page(QuestionScalePage(self, "Domanda di utilità", "Quanto ti è sembrato utile e/o informativo questo contenuto?"))

            self.add_page(TextPage(self, "Ben fatto!", "Per concludere con questo video, compila un questionario sulla valutazione dell'engagement (Video Engagement Scale, o VES).\n" + VES_intro, "Avanti"))

            for item in VES:
                self.add_page(QuestionScalePage(self, "Video Engagement Scale (" + str(i+1) + " di " + str(len(VES)) + ")", item, scale=[str(i+1) for i in range(7)]))

        self.add_page(TextPage(self, "Fin.", "Il nostro esperimento si è concluso, grazie mille per aver partecipato.\nPremi Fine per uscire.", "Fine", button_slot=self.save_and_close))
        
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
            if self.eyeTracker is not None:
                self.participant.add_answer("EyeTracker_Start_Tracker_Time", self.eyeTracker.time())
            
    def stop_capture(self):
        if self.webcamRecorder is not None:
            self.webcamRecorder.stop()
        if self.eyeTracker is not None:
            try:
                self.eyeTracker.stop_recording()
            except:
                pass
        if self.screenRecorder is not None:
            self.screenRecorder.stop()
            
    def closeEvent(self, QCloseEvent):
        self.stop_capture()
        if self.temp_dir is not None:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def save_and_close(self):
        self.hide()
        
        msg = LoadingPopup(self.app, "Salvataggio dei dati raccolti...")
                
        if self.participant is not None:
            self.participant.set_session_end_timestamp()
            self.participant.dump_to_file(self.temp_dir)
        
        self.stop_capture()
        
        shutil.copytree(self.temp_dir, self.participant.participant_dir(), dirs_exist_ok=True)
        
        msg.close()
        self.close()
        
def run_main():
    if sys.platform == 'win32':
        os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
        
    app = QApplication(sys.argv)
    
    opening_msg = LoadingPopup(app, "Stiamo caricando le risorse necessarie...")
    window = MainWindow(app)
    window.webcam_selection_window.show()
    opening_msg.reject()
    sys.exit(app.exec_())