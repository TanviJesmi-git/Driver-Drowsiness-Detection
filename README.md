Driver Drowsiness & Distraction Detection System

This repository contains a real-time Driver Drowsiness & Distraction Detection System that uses computer vision (OpenCV, MediaPipe, TensorFlow Lite) to monitor driver alertness by analyzing eye closure, blink patterns, and head posture. It classifies driver states as Alert, Medium Drowsy, Critical Drowsy, or Distracted, and includes an API for modular integration, enabling deployment in different applications such as in-car monitoring or simulation platforms.

Overview

Problem it solves: Drowsy and distracted driving is a leading cause of road accidents. Traditional blink-only detection systems often raise false alarms or miss distraction cues.
Why it’s important/interesting: This project improves accuracy and real-time adaptability by combining:
    Head Pose Estimation → Detects sustained looking down, up, or sideways (captures distraction/microsleep).
    PERCLOS (Percentage of Eye Closure) → A validated fatigue metric measuring eye closure duration, applied only when the driver looks forward.
    Blink Detection (EAR) → Provides real-time eye state for tracking blinks and closures.
    Grace-Period Logic → Prevents false alerts from natural short glances.
    Fast API → Offers programmatic access to drowsiness classification results, making the system extendable to web apps, mobile dashboards, or vehicle integrations.
Together, these modules work as a robust, real-time fatigue monitoring system.


Driver Drowsiness & Distraction Detection System
This repository contains a real-time Driver Drowsiness & Distraction Detection System built with computer vision (OpenCV, MediaPipe, TensorFlow Lite). The system combines head pose estimation, blink detection, and PERCLOS analysis to classify driver states (Alert, Medium, Critical, Distracted) and enhance road safety.

Features
Real-Time Detection: Monitors driver alertness and distraction via webcam.
Head Pose Estimation: Detects driver’s head orientation for distraction analysis.
Blink Detection & Eye Tracking: Measures blink frequency and eye closure duration.
PERCLOS Analysis: Quantifies eye closure percentage to assess drowsiness.
State Classification: Categorizes driver state as Alert, Medium, Critical, or Distracted.
Customizable Alerts: Multi-stage warning system for different drowsiness levels.
Technologies Used
Python 3.x
OpenCV (image processing)
MediaPipe (facial landmarks)
TensorFlow Lite (ML inference)
Docker (optional, for deployment)
Repository Structure
Code
Driver-Drowsiness-Detection/
├── main.py                # Entry point; imports all modules and runs the system
├── eyetracker.py          # Eye tracking and blink detection logic
├── facemeshdetector.py    # Face mesh detection using MediaPipe
├── headposeestimator.py   # Head pose estimation and distraction logic
├── drowsiness_logic.py    # Drowsiness assessment and state classification
├── requirements.txt       # Python dependencies
├── Dockerfile             # Containerization setup (if provided)
├── README.md              # Project documentation
Getting Started
Prerequisites
Python 3.7+
Webcam
pip
Installation
Clone the repository:

bash
git clone https://github.com/TanviJesmi-git/Driver-Drowsiness-Detection.git
cd Driver-Drowsiness-Detection
Install dependencies:

bash
pip install -r requirements.txt
(Optional) Run with Docker:

bash
docker build -t drowsiness-detector .
docker run --rm -it --device=/dev/video0 drowsiness-detector
Usage
Start the System:

bash
python main.py
All core modules (eyetracker.py, facemeshdetector.py, headposeestimator.py, drowsiness_logic.py) are imported and orchestrated by main.py.
Output:

The driver’s state (Alert, Medium, Critical, Distracted) is displayed in real time.
Alerts are triggered based on state changes.
How It Works
Face Mesh Detection: Locates facial landmarks for robust tracking.
Eye Tracking & Blink Detection: Analyzes eye aspect ratio and blinking patterns.
Head Pose Estimation: Determines if the driver is distracted (not facing forward).
Drowsiness Logic: Combines blink/eye data and head pose to perform PERCLOS analysis and state classification.
Customization
Tune thresholds and parameters directly in drowsiness_logic.py or main.py.
Modify detection logic or add new features by extending the module files.
Contributing
Contributions and issues are welcome! Please open an issue or pull request for suggestions and improvements.

License
This project is licensed under the MIT License. See LICENSE for details.

Author
Tanvi Jesmi
Let me know if you want a sample output, diagrams, or API docs included!

How It Works
Face Mesh Detection: Locates facial landmarks using MediaPipe for robust tracking.
Eye Tracking & EAR Calculation: Computes the Eye Aspect Ratio (EAR) from eye landmarks to measure blink frequency and eye closure duration.
PERCLOS Analysis: Uses EAR values to calculate the Percentage of Eye Closure (PERCLOS), a reliable indicator of drowsiness.
Head Pose Estimation: Determines if the driver is distracted by estimating head orientation.
Adaptive State Classification: Combines PERCLOS-based drowsiness detection and head pose estimation to deliver a real-time, adaptable assessment of the driver’s alertness and distraction level.
Let me know if you’d like this integrated into the full README or want further adjustments!

