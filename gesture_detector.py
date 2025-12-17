import math

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detect_gesture(landmarks):
    """
    Logic đơn giản:
    - Open: Các ngón duỗi ra
    - Close: Các ngón co lại
    - Pinch: Ngón cái và trỏ chạm nhau
    """
    if not landmarks:
        return "idle"

    # Index các đầu ngón: 4, 8, 12, 16, 20
    # Index các khớp gốc: 2, 5, 9, 13, 17
    
    tips = [4, 8, 12, 16, 20]
    bases = [2, 5, 9, 13, 17]
    
    distances = []
    for tip, base in zip(tips, bases):
        distances.append(calculate_distance(landmarks[tip], landmarks[base]))
    
    # Khoảng cách ngón cái và trỏ (cho Pinch)
    thumb_index_dist = calculate_distance(landmarks[4], landmarks[8])

    # --- LOGIC ---
    # 1. Pinch (Kẹp)
    if thumb_index_dist < 0.05: 
        return "pinch"
    
    # 2. Open (Mở)
    fingers_open = 0
    for d in distances[1:]: # Bỏ qua ngón cái check riêng
        if d > 0.1:
            fingers_open += 1
    if fingers_open >= 3:
        return "open"
        
    # 3. Close (Nắm)
    fingers_closed = 0
    for d in distances[1:]:
        if d < 0.08:
            fingers_closed += 1
    if fingers_closed >= 3:
        return "close"

    return "idle"
