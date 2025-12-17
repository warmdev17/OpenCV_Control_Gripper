import cv2

class UIDebugger:
    def __init__(self, window_name="Robot Controller"):
        self.window_name = window_name

    def draw(self, frame, landmarks, gesture, angles, fps):
        if frame is None: return

        # Vẽ điểm khớp tay
        h, w, _ = frame.shape
        if landmarks:
            for lm in landmarks:
                cx, cy = int(lm[0] * w), int(lm[1] * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Vẽ bảng thông tin
        cv2.rectangle(frame, (0, 0), (220, 150), (0, 0, 0), -1)
        
        white = (255, 255, 255)
        green = (0, 255, 0)
        
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, white, 2)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, green, 2)
        
        if angles:
            cv2.putText(frame, f"Base: {angles[0]}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, white, 1)
            cv2.putText(frame, f"Shoulder: {angles[1]}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, white, 1)
            cv2.putText(frame, f"Elbow: {angles[2]}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, white, 1)
            # Gripper
        
        cv2.imshow(self.window_name, frame)

    def close(self):
        cv2.destroyAllWindows()
