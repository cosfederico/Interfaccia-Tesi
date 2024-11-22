import os
import json

class VideosManager:
    def __init__(self, videos_folder='videos'):
        self.videos_folder = videos_folder
        
        if not os.path.exists(self.videos_folder):
            raise NotADirectoryError("Cartella dei video specificata inesistente.")
        
        self.contents = next(os.walk(self.videos_folder))[1]
        
        if len(self.contents) == 0:
            raise RuntimeError("Cartella dei video specificata vuota.\nPer favore carica dei video da riprodurre e riavvia il programma.")
        
        self.types = ['real', 'fake']
        self.genders = ['M', 'F']
        
        self.features = (self.contents, self.types, self.genders)
        self.sizes = [len(feature) for feature in self.features]
    
    def getVideoFeatures(self, participant_id:int) -> list:
        selected_features = []
        for feature, size in zip(self.features, self.sizes):
            selected_features.append(feature[participant_id % size])
            participant_id = participant_id // size
        return selected_features
    
    def getVideoPath(self, participant_id:int) -> str:
        
        folder_path = os.path.join(self.videos_folder, *self.getVideoFeatures(participant_id))                
        
        if not os.path.exists(folder_path):
            raise NotADirectoryError("La struttura di cartelle per il video selezionato non è corretta, dovrebbe essere: " + folder_path)
        
        videos = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith('.mp4') or f.endswith('.avi')
        ]
                
        return videos[0]
    
    def getVideoName(self, participant_id:int) -> str:
        return self.getVideoFeatures(participant_id)[0]
    
    def getVideoType(self, participant_id:int) -> str:
        return self.getVideoFeatures(participant_id)[1]      
    
    def getVideoGender(self, participant_id:int) -> str:
        return self.getVideoFeatures(participant_id)[2]      
    
    def getVideoQuestions(self, participant_id:int, filename='questions.json'):
        path = os.path.join(self.videos_folder, self.getVideoName(participant_id))
        questions = None
        try:
            with open(os.path.join(path, filename), 'r', encoding='UTF-8') as f:
                questions = json.load(f)
        except FileNotFoundError:
            print("File delle domande non trovato per il video " + path + ", no questions will be asked")
        except:
            raise Exception("File delle domande invalido per il video\n\n" + path)
        return questions