class LandmarkFilter:
    def __init__(self, alpha=0.35):
        self.alpha = alpha
        self.prev_landmarks = None

    def filter(self, landmarks):
        """
        Áp dụng bộ lọc EMA (Exponential Moving Average) để giảm rung.
        """
        if landmarks is None:
            self.prev_landmarks = None
            return None

        if self.prev_landmarks is None:
            self.prev_landmarks = landmarks
            return landmarks

        filtered = []
        for i in range(21):
            curr = landmarks[i]
            prev = self.prev_landmarks[i]
            
            # Công thức: New = Alpha * Curr + (1-Alpha) * Prev
            new_x = self.alpha * curr[0] + (1 - self.alpha) * prev[0]
            new_y = self.alpha * curr[1] + (1 - self.alpha) * prev[1]
            new_z = self.alpha * curr[2] + (1 - self.alpha) * prev[2]
            
            filtered.append((new_x, new_y, new_z))

        self.prev_landmarks = filtered
        return filtered
