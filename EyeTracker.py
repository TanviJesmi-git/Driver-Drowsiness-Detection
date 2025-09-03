import cv2
import numpy as np
import math
from collections import deque

class EyeTracker:
    def __init__(self, smooth_window=5):
        # Standard Mediapipe FaceMesh eye landmark indices
        self.right_eye_idx = [362, 385, 387, 263, 373, 380]
        self.left_eye_idx = [33, 160, 158, 133, 153, 144]

        # Smoothing buffer for EAR values
        self.smooth_window = smooth_window
        self.ear_history = deque(maxlen=smooth_window)

    def euclidean_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def calculate_ear(self, image, landmarks):
        h, w, _ = image.shape

        def get_point(idx):
            lm = landmarks[idx]
            return int(lm.x * w), int(lm.y * h)

        # Extract points for right eye
        r_points = [get_point(idx) for idx in self.right_eye_idx]
        # Extract points for left eye
        l_points = [get_point(idx) for idx in self.left_eye_idx]

        # EAR formula for right eye
        rEAR = (self.euclidean_distance(r_points[1], r_points[5]) +
                self.euclidean_distance(r_points[2], r_points[4])) / (2.0 * self.euclidean_distance(r_points[0], r_points[3]))

        # EAR formula for left eye
        lEAR = (self.euclidean_distance(l_points[1], l_points[5]) +
                self.euclidean_distance(l_points[2], l_points[4])) / (2.0 * self.euclidean_distance(l_points[0], l_points[3]))

        ear = (rEAR + lEAR) / 2.0

        # Apply smoothing
        self.ear_history.append(ear)
        smoothed_ear = sum(self.ear_history) / len(self.ear_history)

        return smoothed_ear, r_points, l_points

    def draw_eye_boxes(self, image, r_points, l_points):
        # Draw contours around both eyes using landmarks
        cv2.polylines(image, [np.array(r_points, dtype=np.int32)], True, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.polylines(image, [np.array(l_points, dtype=np.int32)], True, (0, 255, 255), 1, cv2.LINE_AA)
