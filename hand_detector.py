import cv2
import mediapipe as mp
import sys

class HandDetector:
    def __init__(self, confidence=0.7):
        try:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=confidence,
                min_tracking_confidence=confidence
            )
            print("[INFO] Mediapipe Hands loaded successfully!")
        except Exception as e:
            print(f"[ERROR] Không thể khởi tạo MediaPipe: {e}")
            sys.exit(1)

    def detect(self, frame):
        if frame is None:
            return None

        # Chuyển sang RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

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
