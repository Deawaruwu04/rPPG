import cv2
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt
import mediapipe as mp
from collections import deque

# Fungsi untuk Bandpass Filter
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Parameter
frame_rate = 30  # Frame rate dari webcam
buffer_size = 300  # Jumlah frame yang digunakan untuk analisis
rppg_signal = deque(maxlen=buffer_size)  # Buffer sinyal rPPG
time_data = deque(maxlen=buffer_size)  # Buffer waktu

# Inisialisasi Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Inisialisasi Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam tidak dapat diakses!")
    exit()

# Setup Plot Matplotlib
plt.style.use('ggplot')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Konfigurasi Plot Sinyal
ax1.set_title("Sinyal rPPG (Detak Jantung)")
ax1.set_xlim(0, buffer_size / frame_rate)
ax1.set_ylim(-1, 1)
line_rppg, = ax1.plot([], [], label="rPPG", color="green")
ax1.legend()

ax2.set_title("Sinyal Respirasi")
ax2.set_xlim(0, buffer_size / frame_rate)
ax2.set_ylim(-1, 1)
line_respiration, = ax2.plot([], [], label="Respiration", color="blue")
ax2.legend()

plt.tight_layout()

# Fungsi untuk Update Data ke Plot
def update_plot():
    global rppg_signal, time_data

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Webcam tidak terdeteksi!")
            break

        # Konversi ke RGB untuk Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Deteksi Wajah dengan Mediapipe
        results = face_detection.process(rgb_frame)
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x, y, w_box, h_box = (
                    int(bboxC.xmin * w),
                    int(bboxC.ymin * h),
                    int(bboxC.width * w),
                    int(bboxC.height * h),
                )

                if w_box > 0 and h_box > 0:  # Validasi ukuran ROI
                    roi = frame[max(0, y):min(h, y + h_box), max(0, x):min(w, x + w_box)]
                    green_channel = roi[:, :, 1]
                    mean_green = np.mean(green_channel)
                    rppg_signal.append(mean_green)

                    # Gambar rectangle pada wajah yang terdeteksi
                    cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (255, 0, 0), 2)
                break

        # Simpan waktu
        if len(time_data) == 0:
            time_data.append(0)
        else:
            time_data.append(time_data[-1] + 1 / frame_rate)

        # Filter untuk rPPG dan Respirasi
        if len(rppg_signal) > frame_rate:
            filtered_rppg = bandpass_filter(rppg_signal, 0.7, 4, frame_rate)
            filtered_respiration = bandpass_filter(rppg_signal, 0.1, 0.5, frame_rate)

            # Deteksi puncak pada sinyal rPPG
            peaks, _ = find_peaks(filtered_rppg, distance=frame_rate / 2)
            heart_rate = len(peaks) * 60 / (len(filtered_rppg) / frame_rate)

            # Print Heart Rate
            print(f"Heart Rate: {heart_rate:.2f} BPM")

            # Update Data ke Plot
            line_rppg.set_data(time_data, filtered_rppg[-len(time_data):])
            line_respiration.set_data(time_data, filtered_respiration[-len(time_data):])

            # Update Limit untuk x-axis
            ax1.set_xlim(max(0, time_data[0]), max(buffer_size / frame_rate, time_data[-1]))
            ax2.set_xlim(max(0, time_data[0]), max(buffer_size / frame_rate, time_data[-1]))

            # Pastikan ada data sebelum mengatur ylim
            ax1.set_ylim(min(filtered_rppg) - 0.1, max(filtered_rppg) + 0.1)
            ax2.set_ylim(min(filtered_respiration) - 0.1, max(filtered_respiration) + 0.1)

        # Tampilkan Jendela Webcam
        cv2.imshow('Webcam', frame)

        # Perbarui grafik Matplotlib
        plt.pause(1 / frame_rate)

        # Break loop jika tekan 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Jalankan update_plot untuk menampilkan webcam dan grafik secara real-time
update_plot()