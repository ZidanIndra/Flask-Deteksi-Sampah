---
title: EcoSort AI - Deteksi Sampah
emoji: ♻️
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ♻️ EcoSort AI - Deteksi & Klasifikasi Sampah Cerdas

[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space%20Live-yellow.svg)](https://zidanindraa2-deteksi-sampah.static.hf.space)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-CNN-FF6F00.svg?logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Aplikasi kecerdasan buatan berbasis web untuk mengidentifikasi 12 jenis sampah secara otomatis menggunakan Convolutional Neural Network (CNN). Aplikasi memberikan informasi status daur ulang, klasifikasi organik/anorganik/B3, serta panduan pemilahan sampah ramah lingkungan yang praktis.

🌐 **Demo Live di Hugging Face Space:**  
👉 **[https://zidanindraa2-deteksi-sampah.static.hf.space](https://zidanindraa2-deteksi-sampah.static.hf.space)**

---

## ✨ Fitur Unggulan

- **🎨 UI & UX Modern dengan Tailwind CSS**: Tampilan bersih, intuitif, dan sepenuhnya responsif pada perangkat seluler maupun desktop.
- **🛡️ Sistem Pengaman Objek Non-Sampah (OOD Guard)**:
  - **Deteksi Wajah Manusia**: Haar Cascade menolak objek manusia agar sistem berfokus pada sampah.
  - **Validasi Kualitas Gambar**: Menyaring gambar yang terlalu gelap, *overexposed*, atau latar kosong/polos.
  - **Ambang Batas Keyakinan (70%)**: Prediksi di bawah 70% otomatis ditandai *Bukan Sampah/Tidak Valid* dengan notifikasi peringatan.
- **📸 Prediksi dari Foto (Upload)**: Dukungan *drag-and-drop*, pratinjau instan gambar, dan indikator status *loading*.
- **📹 Pemindaian Kamera Real-Time (WebRTC)**:
  - Berjalan langsung di peramban tanpa membebani server.
  - Fitur *Auto-Scan* setiap 1,5 detik dengan laser HUD interaktif.
  - Snapshot manual dan pemilih kamera depan/belakang.
- **🗂️ Direktori 12 Kategori Sampah Lengkap**:
  - `battery`: Baterai (Limbah B3)
  - `biological`: Sisa Makanan / Organik (Kompos)
  - `brown-glass`: Kaca Cokelat (Daur Ulang)
  - `cardboard`: Kardus / Karton (Daur Ulang)
  - `clothes`: Pakaian & Tekstil (Donasi / Upcycle)
  - `green-glass`: Kaca Hijau (Daur Ulang)
  - `metal`: Kaleng & Logam (Daur Ulang)
  - `paper`: Kertas (Daur Ulang)
  - `plastic`: Plastik (Daur Ulang)
  - `shoes`: Sepatu / Alas Kaki (Upcycle / Donasi)
  - `trash`: Residu Umum (TPA)
  - `white-glass`: Kaca Bening (Daur Ulang)

---

## 📁 Struktur Repositori

```text
Flask-Deteksi-Sampah/
├── app.py                 # Backend Flask, rute web, API klasifikasi, & pengaman OOD
├── model/
│   └── predictWaste12.h5  # Model CNN klasifikasi 12 kelas sampah
├── templates/             # Template Flask Jinja2 dengan Tailwind CSS
│   ├── index.html         # Halaman utama & katalog 12 kategori
│   ├── upload.html        # Halaman upload foto & drag-and-drop
│   ├── result.html        # Halaman hasil klasifikasi & panduan penanganan
│   └── real_time.html     # Halaman pemindai kamera real-time WebRTC
├── static/                # Aset statis & direktori upload lokal
├── hf_space/              # Paket Single Page App untuk Hugging Face Static Space
│   ├── index.html         # SPA Tailwind CSS & WebRTC camera demo
│   └── README.md          # Konfigurasi Space Hugging Face
├── Dockerfile             # Konfigurasi container untuk Docker deployment
├── requirements.txt       # Dependensi Python
└── README.md              # Dokumentasi proyek
```

---

## 🚀 Panduan Menjalankan Secara Lokal

### 1. Clone Repositori
```bash
git clone https://github.com/ZidanIndra/Flask-Deteksi-Sampah.git
cd Flask-Deteksi-Sampah
```

### 2. Buat Lingkungan Virtual & Install Dependensi
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Jalankan Server Flask
```bash
python app.py
```

Buka peramban di `http://localhost:7860` atau `http://localhost:4000`.

---

## 🐳 Menjalankan dengan Docker

```bash
# Build image
docker build -t deteksi-sampah .

# Jalankan container
docker run -p 7860:7860 deteksi-sampah
```

Akses aplikasi di `http://localhost:7860`.

---

## 🌐 Deploy ke Hugging Face Space

### Menggunakan Hugging Face CLI:
```bash
# Login akun Hugging Face
hf auth login

# Deploy Static Space (Gratis)
cd hf_space
hf upload zidanindraa2/deteksi-sampah . --type space
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah lisensi [MIT](LICENSE). Silakan gunakan dan kembangkan untuk edukasi maupun pelestarian lingkungan hidup.
