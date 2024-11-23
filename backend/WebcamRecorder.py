from multiprocessing import Process, Queue, Value
import cv2
import time

def capture_frames(cap_id:int, queue:Queue, recording, idle):
    cap = cv2.VideoCapture(cap_id)
    if not cap.isOpened():
        raise RuntimeError("Unable to open webcam")

    idle.value = True  # Signal that the capture process is ready
    
    while idle.value:
        time.sleep(0.01)
    
    while recording.value:
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Unable to read frame from webcam")
        queue.put(frame)

    # Signal the writer process to stop
    queue.put(None)
    cap.release()

def write_frames(queue:Queue, output_file:str, fps:int, resolution:tuple):
    out = cv2.VideoWriter(
        output_file,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        resolution
    )
    
    while True:
        frame = queue.get()
        if frame is None:
            break
        out.write(frame)

    out.release()

class WebcamRecorder:
    def __init__(self, cap_id, cap=None, output_file='webcam.mp4'):
        super(WebcamRecorder, self).__init__()

        self.cap_id = cap_id
        
        if cap is None:
            cap = cv2.VideoCapture(self.cap_id)    
    
        if not cap.isOpened():
            raise Exception("Webcam not found or unavailable")
        
        self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        self.queue = Queue()
        self.output_file = output_file
        self.recording = Value('b', False)
        self.idle = Value('b', False)

        # Start the capture process immediately
        self.writing_process = None
        self.capture_process = Process(
            target=capture_frames,
            args=(self.cap_id, self.queue, self.recording, self.idle)
        )
        self.capture_process.start()

        # Wait until the capture process signals readiness
        while not self.idle.value:
            time.sleep(0.01)

    def start(self):
        self.recording.value = True
        self.idle.value = False
        self.writing_process = Process(
            target=write_frames,
            args=(self.queue, self.output_file, self.fps, (self.frame_width, self.frame_height))
        )
        self.writing_process.start()

    def stop(self):
        self.idle.value = False
        self.recording.value = False
        if self.capture_process is not None:
            self.capture_process.join()         
        if self.writing_process is not None: 
            self.writing_process.join()      
                    
    def isRecording(self):
        return self.recording.value