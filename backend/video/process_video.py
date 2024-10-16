import libreface
import shutil
import os

this_dir = os.path.join(os.getcwd(), 'backend', 'datasync')
temp_dir = os.path.join(this_dir, 'tmp')

def process_video(subject_dir, device='cuda:0', video_file_name="recording.mp4", output_save_path="face_data.csv"):
    
    video_path = os.path.join(subject_dir, video_file_name)
    libreface.get_facial_attributes(video_path,
                                    device=device,
                                    output_save_path=output_save_path,
                                    temp_dir= temp_dir,
                                    weights_download_dir = this_dir)
    
    shutil.rmtree(temp_dir, ignore_errors=True)
    