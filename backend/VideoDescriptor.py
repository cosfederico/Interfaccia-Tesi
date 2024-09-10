import os

class VideoDescriptor:
    
    def __init__(self, video_path):
        
        self.video_path = video_path
        self.title = os.path.basename(self.video_path)
        self.type = os.path.basename(os.path.dirname(self.video_path))
        self.video_dir = os.path.dirname(os.path.dirname(self.video_path))
        
        self.questions = None
    
    def getQuestions(self):
        if self.questions:
            return self.questions
        questions = []
        try:
            with open(os.path.join(self.video_dir, "questions.txt"), 'r', encoding='UTF-8') as f:
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