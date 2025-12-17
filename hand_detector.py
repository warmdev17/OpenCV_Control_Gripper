import os
import sys

# --- ARCH LINUX / PROTOBUF FIX ---
# Bắt buộc phải đặt dòng này ĐẦU TIÊN để tránh lỗi xung đột thư viện trên Linux
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import numpy as np
import cv2

# --- MEDIAPIPE IMPORT ---
# Khởi tạo biến mp_solutions là None trước
mp_solutions = None
mp_hands = None

try:
    import mediapipe as mp
    
    # Thử import submodule solutions theo nhiều cách khác nhau
    try:
        import mediapipe.solutions as solutions
        mp_solutions = solutions
    except ImportError:
        # Fallback cho một số version cũ hoặc cấu trúc lạ
        try:
            import mediapipe.python.solutions as solutions
            mp_solutions = solutions
        except ImportError:
            # Nếu vẫn không được, thử check trong attributes của mp
            if hasattr(mp, 'solutions'):
                mp_solutions = mp.solutions
    
    if mp_solutions is None:
        raise ImportError("Không thể tìm thấy module 'mediapipe.solutions'")

except ImportError as e:
    print(f"[CRITICAL ERROR] Lỗi import MediaPipe: {e}")
    print("Giải pháp: Kiểm tra lại cài đặt bằng lệnh: pip install mediapipe protobuf==3.20.3")
    sys.exit(1)

class HandDetector:
    def __init__(self, confidence=0.7):
        try:
            # Sử dụng biến mp_solutions đã import an toàn ở trên
            self.mp_hands = mp_solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=confidence,
                min_tracking_confidence=confidence
            )
        except Exception as e:
            print(f"[ERROR] Không thể khởi tạo MediaPipe Hands: {e}")
            print("Chi tiết: Có thể do lỗi phiên bản Protobuf hoặc xung đột hệ thống.")
            sys.exit(1)

    def detect(self, frame):
        """
        Input: BGR frame from OpenCV
        Output: List of 21 (x, y, z) tuples (normalized 0-1) or None
        """
        if frame is None:
            return None

        # Mediapipe cần ảnh RGB
        # Chuyển đổi màu an toàn
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception:
            return None
            
        try:
            results = self.hands.process(frame_rgb)
        except Exception:
            return None

        if results.multi_hand_landmarks:
            # Lấy bàn tay đầu tiên
            hand_lms = results.multi_hand_landmarks[0]
            landmarks = []
            for lm in hand_lms.landmark:
                landmarks.append((lm.x, lm.y, lm.z))
            return landmarks
        return None

    def release(self):
        if hasattr(self, 'hands') and self.hands:
            self.hands.close()
