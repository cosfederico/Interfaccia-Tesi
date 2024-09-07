from datetime import datetime, timezone
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
        
    def dump_to_file(self, dir:str):
        
        # write data csv
        with open(dir+'/data.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=Subject.sep)
            
            fields = ["id", "age", "gender", "english_level"]
            row = [self.id, self.age, self.gender, self.english_level]
            
            for i in range(len(self.video_timestamps)):
                
                fields.append('video' + str(i) + '_name')
                fields.append('video' + str(i) + '_start_timestamp')
            
                row.append(self.video_names[i])
                row.append(self.video_timestamps[i])
                
                for j, answer in enumerate(self.video_answers[i]):
                    fields.append('video' + str(i) + '_answer' + str(j))
                    fields.append('video' + str(i) + '_answer' + str(j) + '_timestamp')
                    row.append(answer[0].replace("\n"," ").replace("\t"," "))
                    row.append(answer[1])
                
            writer.writerow(fields)
            writer.writerow(row)