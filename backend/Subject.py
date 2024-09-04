from datetime import datetime, timezone
import os
import csv

class Subject:
    
    data_dir = "data"
    sep = ';'
    
    def __init__(self, id:int):
        self.id = id
        
        self.age = None
        self.gender = None
        self.english_level = None
        
        self.session_start_timestamp = None
        self.session_end_timestamp = None
        self.video_timestamps = []
        self.video_answers = []
        self.video_names = []
        
    def timestamp(self):
        return datetime.now(timezone.utc)
    
    def subject_dir(self):
        return Subject.data_dir + "/" + str(self.id)
        
    def set_data(self, age:int, gender:str, english_level:str):
        self.age=age
        self.gender=gender
        self.english_level=english_level
        
    def set_session_start_timestamp(self):
        self.session_start_timestamp =self.timestamp()
        
    def set_session_end_timestamp(self):
        self.session_end_timestamp =self.timestamp()
        
    def add_video_timestamp(self, video_name:str):
        self.video_names.append(video_name)
        self.video_timestamps.append(self.timestamp())
        
    def add_video_answers(self, answers:list):
        self.video_answers.append(answers)
        
    def dump_to_file(self, file_path:str):
        
        # write data csv
        with open(self.subject_dir()+'/data.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=Subject.sep)
            
            fields = ["id", "age", "gender", "english_level"]
            
            writer.writerow(fields)
            writer.writerow([self.id, self.age, self.gender, self.english_level])
        
        # write answer csv
        for i in range(len(self.video_timestamps)):
            
            with open(self.subject_dir()+'/video'+str(i)+'.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter=Subject.sep)
                
                fields = ['SubjectID', 'video_number', 'video_name', 'start_timestamp']
                row = [self.id, i, self.video_names[i], self.video_timestamps[i]]
                
                for i, answer in enumerate(self.video_answers[i]):
                    fields.append('answer' + str(i))
                    fields.append('timestamp_answer' + str(i))
                    row.append(answer[0].replace("\n"," ").replace("\t"," "))
                    row.append(answer[1])
                
                writer.writerow(fields)
                writer.writerow(row)