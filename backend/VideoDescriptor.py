import os
import random

class VideoDescriptor:
    
    def __init__(self, path):
        
        self.path = path
        self.questions = None
        
        self.real = []
        self.fake = []
        
        for dir in next(os.walk(self.path))[1]:
            
            files:str = os.listdir(os.path.join(self.path, dir))

            for f in files:
                if f.lower().endswith(('.mp4', '.avi')):
                    if dir == "real":
                        self.real = files
                    elif dir == "fake":
                        self.fake = files
                        
        if len(self.real) == 0 or len(self.fake) == 0:
            raise Exception("Nessun video valido trovato in\n\n" + self.path)
    
        questions = []
        try:
            with open(os.path.join(self.path, "questions.txt"), 'r', encoding='UTF-8') as f:
                for line in f:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    questions.append(line)
        except:
            raise Exception("File delle domande non valido o non trovato per il video\n\n" + self.path)
        
        self.questions = questions
    
    def getRandomReal(self):
        return os.path.join(self.path, 'real', random.choice(self.real))
    
    def getRandomFake(self):
        return os.path.join(self.path, 'fake', random.choice(self.fake))
    
    def getRandomVideo(self, real):
        return self.getRandomReal() if real else self.getRandomFake()
    
    def getQuestions(self):
        return self.questions