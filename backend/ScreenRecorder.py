import threading
from PIL import Image
import mss
import cv2
import numpy as np
import queue
import time

class ScreenRecorder(threading.Thread):
    
    def __init__(self, output_file="screen.mp4", fps=24.0, resolution=(1920, 1080), daemon=False):
        super(ScreenRecorder, self).__init__()
                
        self.output_file = output_file
        self.fps = fps
        self.daemon = daemon

        self.buffer = queue.Queue()
        self.resolution = resolution
        print(self.resolution)
        self.recording = False
        self.frame_interval = 1.0 / self.fps
        
        self.out = cv2.VideoWriter(self.output_file, cv2.VideoWriter_fourcc('m','p','4','v'), self.fps, self.resolution)
        
        self.writing_thread = threading.Thread(target=self.start_writing_thread, args=(), daemon=self.daemon)
        self.capture_thread = threading.Thread(target=self.start_capture_thread, args=(), daemon=self.daemon)

    def start_capture_thread(self):
        with mss.mss() as sct:
            next_frame_time = time.time()
                    
            while self.recording:
                current_time = time.time()
                
                if current_time >= next_frame_time:
                    screenshot = sct.grab((0, 0, self.resolution[0], self.resolution[1]))
                    self.buffer.put(screenshot)
                    next_frame_time += self.frame_interval

                # If we're significantly behind, skip to the next correct frame time
                if time.time() > next_frame_time + self.frame_interval:
                    next_frame_time = time.time() + self.frame_interval

    def start_writing_thread(self):
        while self.recording or not self.buffer.empty():
            try:
                screenshot = self.buffer.get(block=True, timeout=self.frame_interval)
            except queue.Empty:
                print("Missed frame")
                continue
            
            # Convert screenshot to frame and write to file
            self.out.write(self.screenshot_to_frame(screenshot))
            
    def run(self):
        self.recording = True
        self.capture_thread.start()
        self.writing_thread.start()
        
    def stop(self):
        self.recording = False
        self.capture_thread.join() 
        self.writing_thread.join()
        self.out.release()
    
    def screenshot_to_frame(self, screenshot):
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        return frame