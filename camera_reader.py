import cv2
import time
import sys
import platform

class CameraReader:
    def __init__(self, device_index=0, width=640, height=480):
        self.device_index = device_index
        self.width = width
        self.height = height
        self.cap = None
        self.fps = 0
        self.prev_time = time.time()

    def open(self):
        # Trên Linux (Arch), backend V4L2 thường ổn định nhất
        system_os = platform.system()
        if system_os == "Windows":
            backend = cv2.CAP_DSHOW
        elif system_os == "Linux":
            backend = cv2.CAP_V4L2
        else:
            backend = cv2.CAP_ANY

        self.cap = cv2.VideoCapture(self.device_index, backend)
        
        if not self.cap.isOpened():
            # Thử lại với backend mặc định nếu thất bại
            self.cap = cv2.VideoCapture(self.device_index)
            
        if not self.cap.isOpened():
            return False

        # Thiết lập độ phân giải
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return True

    def read(self):
        if not self.cap:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Tính FPS
        curr_time = time.time()
        fps_curr = 1 / (curr_time - self.prev_time) if (curr_time - self.prev_time) > 0 else 0
        self.fps = fps_curr
        self.prev_time = curr_time

        # Lật ảnh (Mirror) cho tự nhiên giống soi gương
        return cv2.flip(frame, 1)

    def get_fps(self):
        return self.fps

    def release(self):
        if self.cap:
            self.cap.release()
