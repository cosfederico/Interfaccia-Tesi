from datetime import datetime, timezone
import os
import csv

class Participant:
    
    sep = ';'
    
    def __init__(self, id:int, data_dir:str):
        self.id = id
        self.data_dir = data_dir
        
        self.age = None
        self.gender = None
        self.nationality = None
        self.english_level = None
        
        self.session_start_timestamp = None
        self.session_end_timestamp = None
        
        self.video_name = None
        self.video_type = None
        self.video_start_timestamp = None
        self.video_end_timestamp = None
        
        self.questions = []
        self.answers = []
        
    def timestamp(self):
        return datetime.now(timezone.utc).timestamp()
    
    def participant_dir(self):
        return os.path.join(self.data_dir, str(self.id))
        
    def set_data(self, age:int, gender:str, nationality:str, english_level:str):
        self.age=age
        self.gender=gender
        self.nationality=nationality
        self.english_level=english_level
        
    def set_session_start_timestamp(self):
        self.session_start_timestamp =self.timestamp()
        
    def set_session_end_timestamp(self):
        self.session_end_timestamp =self.timestamp()
        
    def set_video_start_timestamp(self, video_name:str, video_type:str):
        self.video_name = video_name
        self.video_type = video_type
        self.video_start_timestamp = self.timestamp()
        
    def set_video_end_timestamp(self):
        self.video_end_timestamp = self.timestamp()
        
    def add_answer(self, question:str, answer:str):
        question = question.replace('\n', '').replace('\t','')
        self.questions.append(question)
        self.answers.append(answer) 
        self.questions.append(question + "_TS")
        self.answers.append(self.timestamp())
        
    def add_answers(self, questions:list[str], answers:list[str], timestamp_tag):
        if len(questions) != len(answers):
            raise ValueError("Lengths of questions and answers to add to participant don't match - Missing answers?")
        self.questions += [question.replace('\n', '').replace('\t','') for question in questions]
        self.answers += answers
        self.questions.append(timestamp_tag + "_TS")
        self.answers.append(self.timestamp())
        
        
    def dump_to_file(self, dest_dir:str, filename='data.csv'):
        
        with open(os.path.join(dest_dir, filename), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=Participant.sep)
            
            date = datetime.today().strftime('%Y-%m-%d')
            
            fields = ["id", "age", "gender", "nationality", "english_level", "date", "session_start_timestamp", "session_end_timestamp"]
            row = [self.id, self.age, self.gender, self.nationality, self.english_level, date, self.session_start_timestamp, self.session_end_timestamp]
            
            fields += ["video_name", "video_type", "video_start_timestamp", "video_end_timestamp"]
            row += [self.video_name, self.video_type, self.video_start_timestamp, self.video_end_timestamp]
                
            for question, answer in zip(self.questions, self.answers):
                fields.append(question)
                row.append(answer)
                
            writer.writerow(fields)
            writer.writerow(row)