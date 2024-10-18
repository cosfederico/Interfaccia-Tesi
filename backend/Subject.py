from datetime import datetime, timezone
import os
import csv

class Subject:
    
    sep = ';'
    
    def __init__(self, id:int, data_dir:str):
        self.id = id
        self.data_dir = data_dir
        
        self.age = None
        self.gender = None
        self.english_level = None
        
        self.session_start_timestamp = None
        self.session_end_timestamp = None
        
        self.video_start_timestamps = []
        self.video_end_timestamps = []
        self.video_answers = []
        self.video_names = []
        
    def timestamp(self):
        return datetime.now(timezone.utc).timestamp()
    
    def subject_dir(self):
        return os.path.join(self.data_dir, str(self.id))
        
    def set_data(self, age:int, gender:str, english_level:str):
        self.age=age
        self.gender=gender
        self.english_level=english_level
        
    def set_session_start_timestamp(self):
        self.session_start_timestamp =self.timestamp()
        
    def set_session_end_timestamp(self):
        self.session_end_timestamp =self.timestamp()
        
    def add_video_start_timestamp(self, video_name:str):
        self.video_names.append(video_name)
        self.video_start_timestamps.append(self.timestamp())
        
    def add_video_end_timestamp(self):
        self.video_end_timestamps.append(self.timestamp())   
        
    def add_video_answers(self, answers:list):
        self.video_answers.append(answers)
        
    def dump_to_file(self, dest_dir:str):
        
        with open(os.path.join(dest_dir, 'data.csv'), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=Subject.sep)
            
            date = datetime.today().strftime('%Y-%m-%d')
            
            fields = ["id", "age", "gender", "english_level", "date", "session_start_timestamp", "session_end_timestamp"]
            row = [self.id, self.age, self.gender, self.english_level, date, self.session_start_timestamp, self.session_end_timestamp]
            
            for i in range(len(self.video_start_timestamps)):
                
                fields.append('video' + str(i) + '_name')
                fields.append('video' + str(i) + '_start_timestamp')
                fields.append('video' + str(i) + '_end_timestamp')
            
                row.append(self.video_names[i])
                row.append(self.video_start_timestamps[i])
                row.append(self.video_end_timestamps[i])
                
                for j, answer in enumerate(self.video_answers[i]):
                    fields.append('video' + str(i) + '_answer' + str(j))
                    fields.append('video' + str(i) + '_answer' + str(j) + '_timestamp')
                    row.append(answer[0].replace("\n"," ").replace("\t"," "))
                    row.append(answer[1])
                
            writer.writerow(fields)
            writer.writerow(row)