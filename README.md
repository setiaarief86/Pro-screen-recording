# Pro-screen-recording
Screen recording desktop or gaming 

# 馃幀 ProScreen Studio - Screen Recorder



**ProScreen Studio** adalah aplikasi perekam layar (*screen recorder*) berbasis desktop yang ringan, intuitif, dan dilengkapi berbagai pengaturan fleksibel untuk kebutuhan pembuatan konten, tutorial, presentasi, maupun dokumentasi layar.



---



## 鉁� Fitur Utama



Berdasarkan antarmuka aplikasi, ProScreen Studio menyediakan kontrol lengkap untuk setiap sesi perekaman:



### 馃帹 Tampilan & Tema (UI/UX)

- **Light Mode & Dark Mode:** Pengalihan tema terang dan gelap secara instan untuk kenyamanan mata.

- **Indikator Layar (Live FPS Overlay):** Opsi untuk menampilkan penghitung FPS (*Frames Per Second*) secara *real-time* di pojok kiri atas layar selama proses perekaman berlangsung.



### 鈴憋笍 Mode & Durasi Perekaman

- **Rekam Tanpa Batas:** Merekam layar secara terus-menerus hingga dihentikan secara manual melalui tombol *overlay*.

- **Rekam Otomatis (Timer):** Mengatur batas waktu perekaman secara spesifik (**Jam**, **Menit**, dan **Detik**) agar berhenti secara otomatis.



### 馃帴 Kualitas Video & Resolusi

- **Pilihan Resolusi Output Beragam:**

  - Asli Layar (*Native*)

  - 4K UHD (`3840 x 2160`)

  - 2K QHD (`2560 x 1440`)

  - 1080p Full HD (`1920 x 1080`)

  - 720p HD (`1280 x 720`)

  - 640p (`1138 x 640`)

  - 540p qHD (`960 x 540`)

  - 480p SD (`854 x 480`)

  - 360p (`640 x 360`)

- **Target Frame Rate:**

  - `24 FPS` (Sinematik)

  - `30 FPS` (Standar)

  - `60 FPS` (Tinggi)

- **Kontrol Kursor Mouse:** Pilihan untuk **Menampilkan** atau **Menyembunyikan** kursor mouse dalam hasil rekaman.



### 馃帣锔� Pengaturan Sumber Audio

- **Suara Desktop / Aplikasi** (*System Audio*)

- **Mikrofon Saja** (*Microphone Only*)

- **Mikrofon + Suara Desktop** (*Dual Audio*)

- **Tanpa Suara** (*Mute*)



---



## 馃摳 Cuplikan Layar (Screenshots)



| Light Mode | Dark Mode |

| :---: | :---: |

| ![Light Mode](assets/screenshot-light.png) | ![Dark Mode](assets/screenshot-dark.png) |



> **Catatan:** Pastikan Anda menyimpan file gambar *screenshot* di dalam folder `assets/` pada repositori dan menyesuaikan nama filenya.



---



## 馃洜锔� Teknologi yang Digunakan



*(Sesuaikan bagian ini dengan bahasa pemrograman dan library yang Anda pakai)*

- **Bahasa Pemrograman:** Python (Tkinter / PyQt / CustomTkinter) / C# (.NET WinForms / WPF)

- **Perekaman Video & Audio:** OpenCV / FFmpeg / MSS / PyAudio / SoundDevice



---



## 鈿欙笍 Cara Instalasi & Menjalankan



1. **Clone repositori ini**

   ```bash

   git clone https://github.com

   cd proscreen-studio

   ```



2. **Instal dependensi yang diperlukan**

   ```bash

   # Contoh jika menggunakan Python:

   pip install -r requirements.txt

   ```



3. **Jalankan aplikasi**

   ```bash

   # Contoh jika menggunakan Python:

   python main.py

   ```



---



## 馃殌 Cara Penggunaan



1. Pilih tema **Light Mode** atau **Dark Mode** di pojok kanan atas sesuai kenyamanan.

2. Tentukan **Mode & Durasi Perekaman** (tanpa batas atau menggunakan *timer*).

3. Atur **Resolusi Output**, **Target Frame Rate**, dan visibilitas **Kursor Mouse**.

4. Pilih **Sumber Audio** yang ingin direkam.

5. Centang opsi **Indikator Layar** jika ingin memantau performa FPS saat merekam.

6. Klik tombol merah **MULAI PEREKAMAN**.



---



## 馃 Kontribusi



Kontribusi, laporan *bug*, dan permintaan fitur sangat diterima! Silakan buka *Issue* atau kirimkan *Pull Request* pada repositori ini.



## 馃搫 Lisensi



Didistribusikan di bawah lisensi **MIT**. Lihat file `LICENSE` untuk informasi lebih lanjut.


