import os
import random

class VideoDescriptor:
    
    def __init__(self, path):
        
        self.path = path
        self.questions = None
        
        self.real = []
        self.fake = []
        
        for dir in next(os.walk(self.path))[1]:
            if dir == "real":
                self.real = os.listdir(os.path.join(self.path, dir))
            elif dir == "fake":
                self.fake = os.listdir(os.path.join(self.path, dir))
    
    def getRandomReal(self):
        return os.path.join(self.path, 'real', random.choice(self.real))
    
    def getRandomFake(self):
        return os.path.join(self.path, 'fake', random.choice(self.fake))
    
    def getRandomVideo(self, real):
        return self.getRandomReal() if real else self.getRandomFake()
    
    def getQuestions(self):
        if self.questions:
            return self.questions
        questions = []
        try:
            with open(os.path.join(self.path, "questions.txt"), 'r', encoding='UTF-8') as f:
                for line in f:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    questions.append(line)
        except:
            return questions
        finally:
            self.questions = questions
            return questions