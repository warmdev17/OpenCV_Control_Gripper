def get_hand_position(landmarks, frame_width, frame_height):
    """Lấy tọa độ tâm bàn tay (Landmark 9)"""
    if not landmarks:
        return None
        
    lm = landmarks[9] # Khớp dưới ngón giữa
    
    x = int(lm[0] * frame_width)
    y = int(lm[1] * frame_height)
    
    # Kẹp giá trị trong khung hình
    x = max(0, min(frame_width, x))
    y = max(0, min(frame_height, y))
    
    return x, y
