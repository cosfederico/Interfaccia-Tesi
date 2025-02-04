from feat import Detector
import os

def process_video(participant_dir, device='auto', video_file_name="webcam.mp4", output_file_name="face.csv"):
        
    video_path = os.path.join(participant_dir, video_file_name)
    
    detector = Detector(device=device)
    detections = detector.detect_video(video_path, skip_frames=30, face_detection_threshold=0.9)
    detections.to_csv(os.path.join(participant_dir, output_file_name))