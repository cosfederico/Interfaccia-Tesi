from multiprocessing import Process, Queue, Value
import mss
import cv2
import numpy as np
import time
from PIL import Image
import subprocess

def has_nvidia_gpu():
    try:
        # Run `nvidia-smi` to check for NVIDIA GPU
        result = subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # If the command succeeds, an NVIDIA GPU is available
        return result.returncode == 0
    except FileNotFoundError:
        # `nvidia-smi` not found, assume no NVIDIA GPU
        return False

def select_encoder():
    if has_nvidia_gpu():
        return ("h264_nvenc", "fast")
    else:
        return ("mpeg4", "ultrafast")
        

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

    width, height = resolution
    encoder, preset = select_encoder()

    # FFmpeg command for piping
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-f", "rawvideo",  # Input format is raw video
        "-vcodec", "rawvideo",  # Codec is raw video
        "-pix_fmt", "bgr24",  # Pixel format (OpenCV uses BGR by default)
        "-s", f"{width}x{height}",  # Frame size
        "-r", str(fps),  # Frame rate
        "-i", "-",  # Input comes from stdin (pipe)
        "-c:v", encoder,  # Use NVIDIA NVENC encoder
        "-preset", preset,  # Set NVENC preset (fast encoding)
        "-b:v", "5M",  # Set video bitrate to 5 Mbps
        output_file
    ]

    # Start FFmpeg process
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    # Open a video capture device (or replace with your frame source, e.g., mss)
    while True:
        screenshot = queue.get()
        if screenshot is None:  # Sentinel value to terminate
            break

        # Write the frame to FFmpeg's stdin
        ffmpeg_process.stdin.write(screenshot_to_frame(screenshot).tobytes())

    # Clean up
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()  # Wait for FFmpeg to finish encoding

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
        if self.capture_process is not None and self.capture_process.is_alive():
            self.capture_process.join()
        if self.writing_process is not None and self.writing_process.is_alive():        
            self.writing_process.join()
            
    def isRecording(self):
        return self.recording.value