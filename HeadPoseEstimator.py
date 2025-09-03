import cv2
import numpy as np
from enum import Enum


class HeadPoseState(Enum):
    FORWARD = "Looking Forward"
    UP = "Looking Up"
    DOWN = "Looking Down"
    LEFT = "Looking Left"
    RIGHT = "Looking Right"


class HeadPoseEstimator:
    def __init__(self):
        # Key facial landmarks for head pose estimation
        self.pose_landmarks = [33, 263, 1, 61, 291, 199]

        # Thresholds (in degrees, relative to calibration)
        self.pitch_up_threshold = 23     # Above this = Up
        self.pitch_down_threshold = -8   # Below this = Down
        self.yaw_threshold = 20          # Left/Right
        self.forward_tolerance = 10      # ±10° = Forward

        # Calibration
        self.calibration_offset = {'pitch': 0, 'yaw': 0, 'roll': 0}
        self.is_calibrated = False

        # Last known state
        self.last_state = HeadPoseState.FORWARD

    def estimate_pose(self, image, landmarks):
        """Estimate head pose and return angles + head direction"""
        img_h, img_w, _ = image.shape
        face_2d = []
        face_3d = []
        nose_2d = None
        nose_3d = None

        # Extract pose landmarks
        for idx, lm in enumerate(landmarks):
            if idx in self.pose_landmarks:
                if idx == 1:  # Nose tip
                    nose_2d = (lm.x * img_w, lm.y * img_h)
                    nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                x, y = int(lm.x * img_w), int(lm.y * img_h)
                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])

        if len(face_2d) < 6:  # safety check
            return None

        # Convert to numpy arrays
        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        # Camera matrix
        focal_length = 1 * img_w
        cam_matrix = np.array([
            [focal_length, 0, img_h / 2],
            [0, focal_length, img_w / 2],
            [0, 0, 1]
        ])

        # Distortion parameters
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        # Solve PnP
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

        if success:
            # Get rotation matrix and angles
            rmat, _ = cv2.Rodrigues(rot_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

            # Convert to degrees and apply calibration offset
            pitch = (angles[0] * 360) - self.calibration_offset['pitch']
            yaw = (angles[1] * 360) - self.calibration_offset['yaw']
            roll = (angles[2] * 360) - self.calibration_offset['roll']

            # Classify head direction
            direction = self.classify_head_pose(pitch, yaw)

            return {
                'angles': (pitch, yaw, roll),
                'direction': direction,
                'nose_2d': nose_2d
            }

        return None
    

    def classify_head_pose(self, pitch, yaw):
        """Classify head direction from pitch & yaw"""
        if pitch > self.pitch_up_threshold:
            self.last_state = HeadPoseState.UP
        elif pitch < self.pitch_down_threshold:
            self.last_state = HeadPoseState.DOWN
        elif yaw > self.yaw_threshold:
            self.last_state = HeadPoseState.RIGHT
        elif yaw < -self.yaw_threshold:
            self.last_state = HeadPoseState.LEFT
        else:
            if abs(pitch) <= self.forward_tolerance and abs(yaw) <= self.forward_tolerance:
                self.last_state = HeadPoseState.FORWARD

        return self.last_state.value
