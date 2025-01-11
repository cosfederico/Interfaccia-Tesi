import os
import json
import random
from collections import OrderedDict

class VideosManager:
    def __init__(self, videos_folder='videos'):
        self.videos_folder = videos_folder
        
        if not os.path.exists(self.videos_folder):
            os.makedirs(self.videos_folder)

        self.contents = next(os.walk(self.videos_folder))[1]
        
        if len(self.contents) == 0:
            raise RuntimeError("Cartella dei video specificata vuota. Per favore carica dei video da riprodurre per iniziare a usare il programma.\n\nCartella dei video specificata: " + self.videos_folder)
        
        self.features = OrderedDict({
            "content": next(os.walk(self.videos_folder))[1],
            "type": ['real', 'fake'],
            "gender": ['M', 'F']
        })
        
        self.sizes = [len(feature) for feature in self.features.values()]
    
    def getFeaturesNames(self) -> list[str]:
        return list(self.features.keys())
    
    def getVideoFeatures(self, participant_id:int) -> list[str]:
        selected_features = []
        for feature, size in zip(list(self.features.values()), self.sizes):
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
        
        if len(videos) == 0:
            raise FileNotFoundError("No videos found for the selected video combination: " + folder_path)
                
        return random.choice(videos)
    
    def getVideoFeatureByName(self, participant_id:int, feature_name:str) -> str:
        features_names = self.getFeaturesNames()
        if feature_name not in features_names:        
            raise KeyError("No feature found with the given name '" + feature_name + "', known video features are: " + str(features_names))
        video_features = self.getVideoFeatures(participant_id)
        return video_features[features_names.index(feature_name)]

    
    def getVideoQuestions(self, participant_id:int, filename='questions.json') -> dict:
        path = os.path.join(self.videos_folder, self.getVideoFeatureByName(participant_id, 'content'))
        questions = None
        try:
            with open(os.path.join(path, filename), 'r', encoding='UTF-8') as f:
                questions = json.load(f)
        except FileNotFoundError:
            print("File delle domande non trovato per il video " + path + ", no questions will be asked")
        except:
            raise Exception("File delle domande invalido per il video\n\n" + path)
        return questions