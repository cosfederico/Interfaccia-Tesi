import threading
import cv2
import queue

class WebcamRecorder(threading.Thread):
    
    def __init__(self, output_file='webcam.mp4', daemon=True, cap=None):
        super(WebcamRecorder, self).__init__()
        
        self.cap = cap
        
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
            
        if not self.cap.isOpened():
            raise Exception("Webcam non trovata o non disponibile")
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.buffer = queue.Queue()
        self.output_file = output_file
        self.daemon = daemon
        
        self.recording = False
        self.out = None

    def start_capture_thread(self):
        while self.recording:
            ret, frame = self.cap.read()
            
            if not ret:
                raise RuntimeError("Unable to read frame from webcam")
            
            self.buffer.put(frame)
        
    def run(self):
        self.out = cv2.VideoWriter(self.output_file, cv2.VideoWriter_fourcc('m','p','4','v'), self.fps, (self.frame_width,self.frame_height))
        
        self.recording = True
        self.capture_thread = threading.Thread(target=self.start_capture_thread, args=())
        self.capture_thread.start()
        
        while self.recording:
            if (not self.buffer.empty()):
                self.out.write(self.buffer.get())
        
    def stop(self):
        self.recording = False
        
        if self.capture_thread is not None:
            self.capture_thread.join()
        
        while not self.buffer.empty():
                self.out.write(self.buffer.get())
                
        self.cap.release()
        self.out.release()