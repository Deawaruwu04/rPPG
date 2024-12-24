# Sistem Deteksi dan Visualisasi Sinyal rPPG dan Respirasi Berbasis Webcam Secara Real-time
Proyek ini bertujuan untuk mendeteksi sinyal Photoplethysmography (rPPG) dan sinyal respirasi dari
wajah manusia secara real-time menggunakan webcam. Sinyal rPPG digunakan untuk mengukur detak
jantung, sedangkan sinyal respirasi menggambarkan pola pernapasan. Teknologi yang digunakan pada
proyek ini mencakup OpenCV untuk pengolahan video, Mediapipe untuk deteksi wajah, dan Matplotlib
untuk visualisasi sinyal. Proyek ini berfokus pada pemrosesan sinyal berbasis visi, memanfaatkan
bandpass filter untuk menyaring noise, serta algoritma untuk mendeteksi puncak sinyal guna menghitung
parameter fisiologis seperti detak jantung (BPM).
Dengan mengembangkan sistem deteksi sinyal rPPG dan respirasi secara real-
time dari input video, kita akan dapat memvisualisasikan sinyal yang dihasilkan dalam bentuk grafik dan
menghitung detak jantung (BPM) dari sinyal rPPG yang lalu dapat digunakan untuk keperluan lainnya.

![WhatsApp Image 2024-12-23 at 15 10 36 (1)](https://github.com/user-attachments/assets/d782b979-5266-4699-bbd3-40312333ff72)

## Instruksi Instalasi
### 1. Instal Python:
Pastikan Python sudah terinstal pada sistem Anda. Anda bisa mengunduhnya dari python.org jika belum terinstal.
### 2. Instal Paket yang Diperlukan:
Buka terminal atau command prompt dan jalankan perintah berikut untuk menginstal paket-paket yang diperlukan:

`pip install opencv-python numpy scipy matplotlib mediapipe`

Jika Anda menggunakan sistem operasi Windows, pastikan **pip** dalam PATH atau gunakan `python -m pip install` sebagai alternatif.
### 3. Kamera Webcam:
Pastikan Anda memiliki kamera webcam yang dapat diakses oleh sistem Anda. Kode ini menggunakan kamera default (index 0). Jika Anda memiliki lebih dari satu kamera, Anda mungkin perlu mengubah indeks dalam **cv2.VideoCapture(0)**.
### 4. Menjalankan Kode:
Simpan kode dalam file Python.
Buka terminal atau command prompt, navigasikan ke direktori tempat file tersebut disimpan, dan jalankan dengan:

`python rPPG.py`

## Petunjuk Penggunaan:
Setelah menjalankan kode program, sebuah jendela akan terbuka menampilkan feed dari webcam Anda. Jika wajah terdeteksi, akan ada kotak di sekitar wajah dan data detak jantung akan dihitung dan ditampilkan dalam konsol.
Dua plot matplotlib akan diperbarui secara real-time menunjukkan sinyal rPPG (detak jantung) dan sinyal respirasi.
Tekan 'q' pada keyboard untuk menghentikan program.

## Requirements / Dependencies
Nama                           | Fungsi
:-------------------------------      | :-------------
OpenCV          | Pengolahan Video
Mediapipe       | Pendeteksian Wajah
Matplotlib      | Visualisasi Sinyal
NumPy
SciPy

## Logbook Mingguan
Minggu ke-                            | Kegiatan
:-------------------------------      | :-------------
Minggu ke-1 (27-30 November 2024)     | -
Minggu ke-2 (2-8 Desember 2024)       | Melakukan riset dan mencari berbagai referensi mengenai sistem pengukuran sinyal respirasi dan sistem penukuran remote-photopletysmography (rPPG)
Minggu ke-3 (9-15 Desember 2024)      | Menentukan judul project dan mulai mencoba membuat program
Minggu ke-4 (16-22 Desember 2024)     | Melanjutkan progress pembuatan program dan laporan
Minggu ke-5 (23-24 Desember 2024)     | Menyelesaikan program dan laporan serta melakukan pengumpulan


## Anggota Kelompok
NAMA                             | NIM             | ID Github
:------------------------------: | :-------------: | :---------------:
[Muhammad Taqy Abdullah]         | [121140166]     | 166Taqy
[Fadel Malik]                    | [121140167]     | Fadel-Malik
[Dea Lisriani Safitri Waruwu]    | [121140208]     | Deawaruwu04
