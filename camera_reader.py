import cv2
import time

class CameraReader:
    def __init__(self, device_index=0, width=640, height=480):
        self.device_index = device_index
        self.width = width
        self.height = height
        self.cap = None
        self.fps = 0
        self.prev_time = time.time()

    def open(self):
        # Trên Windows, dùng CAP_DSHOW giúp mở camera nhanh hơn và không bị delay
        self.cap = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            # Thử lại chế độ mặc định nếu DSHOW lỗi
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

        # Lật ảnh (Mirror) cho tự nhiên
        return cv2.flip(frame, 1)

    def get_fps(self):
        return self.fps

    def release(self):
        if self.cap:
            self.cap.release()
