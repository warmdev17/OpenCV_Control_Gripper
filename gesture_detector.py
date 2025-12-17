import math

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detect_gesture(landmarks):
    """
    Trả về: 'open', 'close', 'pinch', 'idle'
    """
    if not landmarks:
        return "idle"

    # Các đầu ngón tay: 4(Cái), 8(Trỏ), 12(Giữa), 16(Nhẫn), 20(Út)
    # Các khớp gốc: 2, 5, 9, 13, 17
    
    tips = [4, 8, 12, 16, 20]
    bases = [2, 5, 9, 13, 17]
    
    # Tính khoảng cách từ đầu ngón đến khớp gốc
    distances = []
    for tip, base in zip(tips, bases):
        distances.append(calculate_distance(landmarks[tip], landmarks[base]))
    
    # Ngón cái hơi đặc biệt, dùng khoảng cách đến ngón trỏ để check 'pinch'
    thumb_index_dist = calculate_distance(landmarks[4], landmarks[8])

    # Ngưỡng (Threshold) - Cần tinh chỉnh tùy tay
    # Khoảng cách chuẩn hóa 0.0 - 1.0
    
    # Logic:
    # 1. Pinch: Ngón cái và trỏ rất gần nhau
    if thumb_index_dist < 0.05: 
        return "pinch"
    
    # 2. Open: Các ngón dài (trỏ, giữa, nhẫn, út) đều duỗi thẳng (xa khớp gốc)
    # distance > 0.1 (ngưỡng tùy chỉnh)
    fingers_open = 0
    for d in distances[1:]: # Bỏ qua ngón cái
        if d > 0.1:
            fingers_open += 1
            
    if fingers_open >= 3:
        return "open"
        
    # 3. Close: Các ngón co lại (gần khớp gốc)
    fingers_closed = 0
    for d in distances[1:]:
        if d < 0.08:
            fingers_closed += 1
            
    if fingers_closed >= 3:
        return "close"

    return "idle"
