from multiprocessing import Process, Queue, Value
import mss
import cv2
import numpy as np
import time
from PIL import Image

def capture_frames(queue:Queue, fps:int, resolution:tuple, recording_flag):
    with mss.mss() as sct:
        frame_interval = 1.0 / fps
        next_frame_time = time.time()

        while recording_flag.value:
            
            current_time = time.time()
            if current_time >= next_frame_time:
                screenshot = sct.grab((0, 0, resolution[0], resolution[1]))
                queue.put(screenshot)
                next_frame_time += frame_interval

            if time.time() > next_frame_time + frame_interval:
                next_frame_time = time.time() + frame_interval

        # Signal the writing process to stop
        queue.put(None)

def screenshot_to_frame(screenshot):
    img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    return frame

def write_frames(queue:Queue, output_file:str, fps:int, resolution:tuple):
    out = cv2.VideoWriter(
        output_file,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        resolution
    )

    while True:
        screenshot = queue.get()
        if screenshot is None:  # Sentinel value to terminate
            break

        out.write(screenshot_to_frame(screenshot))

    out.release()

class ScreenRecorder:
    def __init__(self, output_file="screen.mp4", fps=24.0, resolution=(1920, 1080), daemon=False):
        self.output_file = output_file
        self.fps = fps
        self.resolution = resolution
        self.recording_flag = None
        self.frame_queue = Queue() 
        self.recording = Value('b', False)
        
        self.capture_process = None
        self.writing_process = None

    def start(self):
        self.recording.value = True

        self.capture_process = Process(
            target=capture_frames,
            args=(self.frame_queue, self.fps, self.resolution, self.recording)
        )
        self.writing_process = Process(
            target=write_frames,
            args=(self.frame_queue, self.output_file, self.fps, self.resolution)
        )

        self.capture_process.start()
        self.writing_process.start()

    def stop(self):
        self.recording.value = False
        if self.capture_process is not None:
            self.capture_process.join()
        if self.writing_process is not None:        
            self.writing_process.join()
