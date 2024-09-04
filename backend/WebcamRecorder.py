import threading
import cv2
import queue

class WebcamRecorder(threading.Thread):
    
    def __init__(self, output_file, daemon):
        super(WebcamRecorder, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.recording = False
        self.buffer = queue.Queue()
        self.output_file = output_file
        self.daemon = daemon

    def start_capture_thread(self):
        while True:
            _, frame = self.cap.read()
            self.buffer.put(frame)

            if (not self.recording):
                self.cap.release()
                break
        
    def run(self):
        out = cv2.VideoWriter(self.output_file, cv2.VideoWriter_fourcc('m','p','4','v'), self.fps, (self.frame_width,self.frame_height))
        
        t = threading.Thread(target=self.start_capture_thread, args=())
        t.start()
        
        self.recording = True
        while True:            
            if (not self.buffer.empty()):
                out.write(self.buffer.get())
            
            if (not self.recording):
                break
        
        out.release()
        
    def stop(self):
        self.recording = False
