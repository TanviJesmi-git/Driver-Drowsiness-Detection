from fastapi import FastAPI
import cv2
import numpy as np
import requests
import threading

# import your detection modules
from FaceMeshDetector import FaceMeshDetector
from HeadPoseEstimator import HeadPoseEstimator
from EyeTracker import EyeTracker
from main import EnhancedDrowsinessDetector

app = FastAPI(title="Drowsiness Detection Service")

# ---------- Init Models ----------
face_detector = FaceMeshDetector()
head_pose_estimator = HeadPoseEstimator()
eye_tracker = EyeTracker()
drowsiness_detector = EnhancedDrowsinessDetector()

# ---------- Config ----------
MODULE1_URL = "http://module1:8000/enhance_frame/"   # talk to Module 1 inside docker-compose

# ---------- Shared State ----------
latest_result = {"drowsiness_level": "Not Started"}
running = False
thread = None


def get_enhanced_frame(frame: np.ndarray) -> np.ndarray:
    """Send raw frame to Module 1 and get enhanced frame"""
    _, buffer = cv2.imencode(".jpg", frame)
    files = {"file": ("frame.jpg", buffer.tobytes(), "image/jpeg")}
    resp = requests.post(MODULE1_URL, files=files)
    if resp.status_code == 200:
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)
    else:
        print("⚠️ Enhancement failed:", resp.text)
        return frame


def process_frame(image: np.ndarray) -> dict:
    """Run detection pipeline on enhanced frame"""
    results = face_detector.detect_landmarks(image)
    head_direction, ear = "Unknown", 0.0

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            pose_data = head_pose_estimator.estimate_pose(image, landmarks)
            if pose_data:
                head_direction = head_pose_estimator.get_head_direction(pose_data['angles'])
            ear, _, _ = eye_tracker.calculate_ear(image, landmarks)

    # update blink/drowsiness state
    drowsiness_detector.update_blink(ear)
    drowsiness_detector.update_state()
    drowsiness_level, _, blinks = drowsiness_detector.get_status()

    return {
        "drowsiness_level": drowsiness_level,
        "head_direction": head_direction,
        "ear": round(ear, 3),
        "blinks": blinks
    }


def detection_loop():
    global running, latest_result
    cap = cv2.VideoCapture(0)

    while running and cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # enhance with Module 1
        enhanced = get_enhanced_frame(frame)

        # detect drowsiness
        result = process_frame(enhanced)
        latest_result = result

    cap.release()
    running = False


@app.get("/start_detection")
def start_detection():
    """Start detection in background thread"""
    global running, thread
    if running:
        return {"message": "Detection already running"}

    running = True
    thread = threading.Thread(target=detection_loop, daemon=True)
    thread.start()
    return {"message": "Detection started"}


@app.get("/status")
def get_status():
    """Get latest detection result"""
    return latest_result


@app.get("/stop_detection")
def stop_detection():
    """Stop detection loop"""
    global running
    running = False
    return {"message": "Detection stopped", "last_result": latest_result}
