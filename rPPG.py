import cv2
import matplotlib.pyplot as plt
import mediapipe as mp

# Parameter
frame_rate = 30  # Frame rate dari webcam

# Inisialisasi Webcam
cap = cv2.VideoCapture(0)

# Inisialisasi Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

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

# Loop Webcam dengan Deteksi Wajah
while True:
    ret, frame = cap.read()
    if not ret:
        print("Webcam tidak terdeteksi!")
        break

    frame, face_data = detect_face(frame)
    cv2.imshow("Webcam", frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
