import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import csv
from datetime import datetime

# EAR calculation
def calculate_ear(landmarks, eye_indices):
    p1 = np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y])
    p2 = np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y])
    p3 = np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])
    p4 = np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y])
    p0 = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    p5 = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])
    vert = np.linalg.norm(p2 - p4) + np.linalg.norm(p3 - p5)
    horiz = np.linalg.norm(p0 - p1)
    ear = vert / (2.0 * horiz)
    return ear

# Setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

st.title("🧠 Personal Stress Meter")
st.write("This app tracks eyelid openness to estimate stress or fatigue in real time.")

cap = cv2.VideoCapture(0)
stframe = st.empty()
ear_deque = deque(maxlen=30)

# Write CSV header if file is empty / doesn't exist
try:
    with open("stress_log.csv", mode="x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "avg_ear", "stress_level"])
except FileExistsError:
    pass  # File already exists

# Main loop
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye_idx = [33, 160, 158, 133, 153, 144]
            right_eye_idx = [362, 385, 387, 263, 373, 380]

            left_ear = calculate_ear(face_landmarks.landmark, left_eye_idx)
            right_ear = calculate_ear(face_landmarks.landmark, right_eye_idx)
            avg_ear = (left_ear + right_ear) / 2
            ear_deque.append(avg_ear)

            # Calculate stress based on EAR deviation from normal
            avg_ear = np.mean(ear_deque)
            # Based on your data, normal EAR is around 1.0-1.1
            # Lower EAR values indicate more closed eyes (tiredness/stress)
            # Map EAR range (0.8-1.2) to stress range (1.0-0.0)
            baseline_ear = 1.05  # Normal relaxed eye openness
            sensitivity = 0.3    # How much EAR change affects stress
            
            # Higher stress when EAR is below baseline (more closed eyes)
            stress_level = max(0, min(1, (baseline_ear - avg_ear) / sensitivity))
            
            # Add some debug info
            print(f"EAR: {avg_ear:.3f}, Stress: {stress_level:.3f}")

            # Show overlay
            cv2.putText(frame, f"EAR: {avg_ear:.3f}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Stress Level: {stress_level:.2f}", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Log to CSV
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open("stress_log.csv", mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, avg_ear, stress_level])

    stframe.image(frame, channels="BGR")

cap.release()
