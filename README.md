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

Comparison with Existing Systems:

Traditional Blink-only Systems
❌ Often raise false alarms during normal blinks.
❌ Cannot detect distraction (head turning up, down, left, right).
❌ Limited adaptability with static thresholds.
❌ Usually standalone, no external integration.
⚡ Basic blink counting, limited real-time capability.
Our System (Blink + Head Pose + PERCLOS + API)
✅ Higher detection accuracy by combining multiple cues (blinks, head pose, PERCLOS).
✅ Detects distraction by monitoring head directions (left, right, up, down).
✅ Dynamic and adaptable with PERCLOS-based thresholds + grace-period logic.
✅ Provides an API for deployment in external apps, vehicles, or monitoring dashboards.
✅ Runs at ~20 FPS with integrated metrics for real-time adaptability.

🛠️ Tech Stack

Languages:Python
Libraries/Frameworks:OpenCV,MediaPipe,NumPy,FastAPI 
Tools:Git & GitHub,Virtual Environment (venv),docker
IDE: VS Code
