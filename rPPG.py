import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
from scipy.signal import butter, lfilter
from collections import deque

# Parameter
frame_rate = 30  # Frame rate dari webcam
buffer_size = 300  # Jumlah frame yang digunakan untuk analisis

# Inisialisasi Webcam
cap = cv2.VideoCapture(0)

# Inisialisasi Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Fungsi untuk Bandpass Filter
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# Fungsi Deteksi Wajah
def detect_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            h, w, c = frame.shape
            x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (255, 0, 0), 2)
            return frame, (x, y, w_box, h_box)
    return frame, None

# Buffer untuk sinyal rPPG
rppg_signal = deque(maxlen=buffer_size)

# Ekstraksi sinyal hijau dari ROI
def extract_signal(roi):
    green_channel = roi[:, :, 1]
    return np.mean(green_channel)

# Integrasi analisis sinyal dengan deteksi wajah
while True:
    ret, frame = cap.read()
    if not ret:
        print("Webcam tidak terdeteksi!")
        break

    frame, face_data = detect_face(frame)
    if face_data:
        x, y, w_box, h_box = face_data
        roi = frame[y:y + h_box, x:x + w_box]

        # Ekstrak sinyal hijau dan masukkan ke buffer
        mean_green = extract_signal(roi)
        rppg_signal.append(mean_green)

        # Terapkan filter jika buffer mencukupi
        if len(rppg_signal) > frame_rate:
            filtered_signal = bandpass_filter(rppg_signal, 0.7, 4, frame_rate)
            print(f"Filtered Signal: {filtered_signal[-10:]}")  # Contoh output sinyal yang difilter

    cv2.imshow("Webcam", frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
