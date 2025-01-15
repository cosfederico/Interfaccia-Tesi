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
        self.education = None
        
        self.session_start_timestamp = None
        self.session_end_timestamp = None
        
        self.questions = []
        self.answers = []
        
    def timestamp(self):
        return datetime.now(timezone.utc).timestamp()
    
    def participant_dir(self):
        return os.path.join(self.data_dir, str(self.id))
        
    def set_data(self, age:int, gender:str, nationality:str, education:str):
        self.age=age
        self.gender=gender
        self.nationality=nationality
        self.education=education
        
    def set_session_start_timestamp(self):
        self.session_start_timestamp =self.timestamp()
        
    def set_session_end_timestamp(self):
        self.session_end_timestamp =self.timestamp()
        
    def set_video_start_timestamp(self):
        self.questions.append(self.uniquify("Video Start Timestamp"))
        self.answers.append(self.timestamp())
        
    def set_video_end_timestamp(self):
        self.questions.append(self.uniquify("Video End Timestamp"))
        self.answers.append(self.timestamp())

    def uniquify(self, question):
        unique_question = question
        counter = 1
        while unique_question in self.questions:
            unique_question = question + str(counter)
            counter += 1
        return unique_question
        
    def add_answer(self, question:str, answer:str, save_timestamp=True):
        question = question.replace('\n', '').replace('\t','')
        question = self.uniquify(question)
        self.questions.append(question)
        self.answers.append(answer)
        if save_timestamp:
            self.questions.append(question + "_TS")
            self.answers.append(self.timestamp())
        
    def add_answers(self, questions:list[str], answers:list[str], timestamp_tag):
        if len(questions) != len(answers):
            raise ValueError("Lengths of questions and answers to add to participant don't match - Missing answers?")
        questions = [question.replace('\n', '').replace('\t','') for question in questions]
        questions = [self.uniquify(question) for question in questions]
        self.questions += questions
        self.answers += answers
        self.questions.append(timestamp_tag + "_TS")
        self.answers.append(self.timestamp())
        
    def dump_to_file(self, dest_dir:str, filename='data.csv'):
        
        with open(os.path.join(dest_dir, filename), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=Participant.sep)
            
            date = datetime.today().strftime('%Y-%m-%d')
            
            fields = ["Id", "Age", "Gender", "Nationality", "Education", "Date", "Session Start Timestamp", "Session End Timestamp"]
            row = [self.id, self.age, self.gender, self.nationality, self.education, date, self.session_start_timestamp, self.session_end_timestamp]
                
            for question, answer in zip(self.questions, self.answers):
                fields.append(question)
                row.append(answer)
                
            writer.writerow(fields)
            writer.writerow(row)