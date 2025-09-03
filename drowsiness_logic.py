import time
from collections import deque

class EnhancedDrowsinessDetector:
    def __init__(self, ear_threshold=0.26, window_seconds=20):
        self.ear_threshold = ear_threshold
        self.drowsiness_level = "NOT DROWSY"
        self.color = (0, 255, 0)

        # Store (timestamp, is_closed) for last `window_seconds`
        self.window_seconds = window_seconds
        self.eye_history = deque()

        # Head direction tracking
        self.last_direction = "Looking Forward"
        self.direction_start_time = time.time()
        self.away_start_time = None
        self.away_period = 1.0  # seconds
        self.min_perclos_time = 12  # seconds of forward data required
        self.avg_fps = 20           # based on your measured FPS



    def update_blink(self, ear, head_direction):
    
     now = time.time()
     is_closed = ear < self.ear_threshold

     if head_direction == "Looking Forward":
        # Reset away timer since we're back to forward
        self.away_start_time = None  

        # Track closure history
        self.eye_history.append((now, is_closed))

        # Keep only recent frames
        while self.eye_history and now - self.eye_history[0][0] > self.window_seconds:
            self.eye_history.popleft()

     else:
        # Start grace period timer if just looked away
        if self.away_start_time is None:
            self.away_start_time = now

        # If away longer than grace period → reset PERCLOS
        if now - self.away_start_time > self.away_period:
            self.eye_history.clear()

    def calculate_perclos(self):
        if not self.eye_history:
         return 0.0

        now = time.time()
        weighted_closed = 0
        weighted_total = 0

        for t, closed in self.eye_history:
         age = now - t
        # weight recent frames higher
         weight = 2 if age <= 10 else 1
         weighted_total += weight
         if closed:
            weighted_closed += weight

        return weighted_closed / weighted_total if weighted_total > 0 else 0.0

    def update_head_direction(self, head_direction):
        """Track sustained head direction."""
        now = time.time()
        if head_direction != self.last_direction:
            self.last_direction = head_direction
            self.direction_start_time = now

        sustained_time = now - self.direction_start_time
        return head_direction, sustained_time

    def update_state(self, head_direction):
     head_direction, sustained_time = self.update_head_direction(head_direction)
     perclos = self.calculate_perclos()
     #eyes_closed_now = self.eye_history[-1][1] if self.eye_history else False

    # ---- Critical: head down/up too long ----
     if head_direction in ["Looking Down", "Looking Up"] and sustained_time > 2.5:
        self.drowsiness_level = "CRITICAL"
        self.color = (0, 0, 255)

    # ---- Distraction: left/right too long ----
     elif head_direction in ["Looking Left", "Looking Right"] and sustained_time > 3:
        self.drowsiness_level = "DISTRACTION"
        self.color = (0, 165, 255)

     elif head_direction == "Looking Forward":
      min_frames_required = int(self.min_perclos_time * self.avg_fps)

      if len(self.eye_history) >= min_frames_required:
        if perclos > 0.40:
            self.drowsiness_level = "CRITICAL"
            self.color = (0, 0, 255)
        elif perclos > 0.25:
            self.drowsiness_level = "MEDIUM"
            self.color = (0, 255, 255)
        else:
            self.drowsiness_level = "NOT DROWSY"
            self.color = (0, 255, 0)
      else:
        # Not enough data yet → safe default
        self.drowsiness_level = "NOT DROWSY"
        self.color = (0, 255, 0)

     else:
        # If no valid state, stay normal
        self.drowsiness_level = "NOT DROWSY"
        self.color = (0, 255, 0)

    def get_status(self):
        return self.drowsiness_level, self.color, self.calculate_perclos()
