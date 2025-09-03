import cv2
import time
import numpy as np
from FaceMeshDetector import FaceMeshDetector 
from HeadPoseEstimator import HeadPoseEstimator
from EyeTracker import EyeTracker
from drowsiness_logic import EnhancedDrowsinessDetector

class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.fps = 0
        self.history = []
        self.all_fps = []  # store all fps values for logging

    def update(self):
        end_time = time.time()
        time_diff = end_time - self.start_time
        inst_fps = 1 / time_diff if time_diff > 0 else 0
        self.start_time = end_time

        self.history.append(inst_fps)
        if len(self.history) > 10:
            self.history.pop(0)

        self.fps = sum(self.history) / len(self.history)
        self.all_fps.append(self.fps)
        return self.fps

    def get_metrics(self):
        if not self.all_fps:
            return 0, 0, 0
        avg_fps = sum(self.all_fps) / len(self.all_fps)
        min_fps = min(self.all_fps)
        max_fps = max(self.all_fps)
        return avg_fps, min_fps, max_fps


class DisplayManager:
    @staticmethod
    def draw_drowsiness_box(image, drowsiness_level, color):
        box_x, box_y = 20, 90
        box_width, box_height = 300, 80
        cv2.rectangle(image, (box_x, box_y), (box_x + box_width, box_y + box_height), (50, 50, 50), -1)
        cv2.rectangle(image, (box_x, box_y), (box_x + box_width, box_y + box_height), color, 3)
        text = f"DROWSINESS: {drowsiness_level}"
        font_scale, thickness = 0.8, 2
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        text_x = box_x + (box_width - text_size[0]) // 2
        text_y = box_y + (box_height + text_size[1]) // 2
        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

    @staticmethod
    def draw_info(image, head_direction, ear, drowsiness_level, color, fps, perclos):
        cv2.putText(image, f"Head Direction: {head_direction}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(image, f'EAR: {np.round(ear, 3)}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        DisplayManager.draw_drowsiness_box(image, drowsiness_level, color)
        cv2.putText(image, f'FPS: {int(fps)}', (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(image, f'PERCLOS: {perclos*100:.1f}%', 
                (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)


class MainApplication:
    def __init__(self):
        self.face_detector = FaceMeshDetector()
        self.head_pose_estimator = HeadPoseEstimator()
        self.eye_tracker = EyeTracker()
        self.drowsiness_detector = EnhancedDrowsinessDetector()
        self.fps_counter = FPSCounter()
        self.cap = cv2.VideoCapture(0)
        self.target_fps = 30
        self.frame_time = 1 / self.target_fps

    def process_frame(self, image):
        results = self.face_detector.detect_landmarks(image)
        head_direction, ear = "Unknown", 0.0

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
              landmarks = face_landmarks.landmark
              pose_data = self.head_pose_estimator.estimate_pose(image, landmarks)
              if pose_data:
                pitch, yaw, roll = pose_data['angles']
                head_direction = pose_data['direction']

                # Debug print
                print(f"Head Direction: {head_direction:<15} | Pitch: {pitch:6.1f}° | Yaw: {yaw:6.1f}° | Roll: {roll:6.1f}°")

                
            
            # EAR (eye aspect ratio)
            ear, r_points, l_points = self.eye_tracker.calculate_ear(image, landmarks)
            self.eye_tracker.draw_eye_boxes(image, r_points, l_points)

        return head_direction, ear

    def run(self):
        print("Starting Enhanced Blink-based Drowsiness Detection System...")
        print("Target FPS:", self.target_fps, "Press ESC to exit")

        while self.cap.isOpened():
            start_time = time.time()
            success, image = self.cap.read()
            if not success:
                continue

            fps = self.fps_counter.update()
            image = cv2.flip(image, 1)

            head_direction, ear = self.process_frame(image)

            self.drowsiness_detector.update_blink(ear, head_direction)
            self.drowsiness_detector.update_state(head_direction)
            drowsiness_level, color, perclos = self.drowsiness_detector.get_status()

            DisplayManager.draw_info(image, head_direction, ear, drowsiness_level, color, fps, perclos)
            cv2.imshow("Enhanced Blink-based Drowsiness Detection", image)


            if cv2.waitKey(1) & 0xFF == 27:
                break

            elapsed = time.time() - start_time
            if elapsed < self.frame_time:
                time.sleep(self.frame_time - elapsed)

        self.cap.release()
        cv2.destroyAllWindows()

        avg_fps, min_fps, max_fps = self.fps_counter.get_metrics()
        print(f"Application closed. Performance Metrics -> Avg FPS: {avg_fps:.2f}, Min FPS: {min_fps:.2f}, Max FPS: {max_fps:.2f}")


if __name__ == "__main__":
    app = MainApplication()
    app.run()
