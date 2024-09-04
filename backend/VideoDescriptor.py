import os
import random

class VideoDescriptor:
    
    video_dir = "videos"
    
    def __init__(self, name):
        self.name = name
        self.script = None
        self.questions = None
        
        self.real = []
        self.fake = []
        
        for dir in next(os.walk(self.fullpath()))[1]:
            if dir == "real":
                self.real = os.listdir(self.fullpath() +"/"+ dir)
            elif dir == "fake":
                self.fake = os.listdir(self.fullpath() +"/"+ dir)            
    
    def fullpath(self):
        return  VideoDescriptor.video_dir  + "/" + self.name
    
    def fake_video_paths(self):
        fake_videos = []
        for fake_video_name in self.fake:
            fake_videos.append(self.fullpath() + "/fake/" + fake_video_name)
        return fake_videos
    
    def real_video_paths(self):
        real_videos = []
        for real_video_name in self.real:
            real_videos.append(self.fullpath() + "/real/" + real_video_name)
        return real_videos
        
    def getScript(self):
        if self.script:
            return self.script
        self.script = ""
        try:
            with open(self.video_dir + "/" + self.name +"/script.txt", 'r', encoding='UTF-8') as f:
                for line in f:
                    self.script += line
        finally:
            return self.script
    
    def getQuestions(self):
        if self.questions:
            return self.questions
        questions = []
        try:
            with open(self.fullpath() + "/questions.txt", 'r', encoding='UTF-8') as f:
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
    
    def getReal(self):
        return self.fullpath() + "/real/" + self.real[0]
        
    def getRandomFake(self):
        return self.fullpath() + "/fake/" + random.choice(self.fake)