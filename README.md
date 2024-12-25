# Deteksi Sampah Menggunakan Flask

Aplikasi ini bertujuan untuk mendeteksi jenis sampah berdasarkan gambar yang diunggah oleh pengguna. Model yang digunakan untuk klasifikasi gambar adalah model CNN yang dilatih dengan dataset tertentu, dan model ini disimpan dalam format `.h5`. Aplikasi ini dibangun menggunakan Flask sebagai framework web.

## Fitur

- Mengunggah gambar sampah untuk diklasifikasikan.
- Menggunakan model CNN yang telah dilatih untuk mendeteksi jenis sampah.
- Klasifikasi hasil dalam kategori berikut:
  - **Output Classes**:  
    `["battery", "biological", "brown-glass", "cardboard", "clothes", "green-glass", "metal", "paper", "plastic", "shoes", "trash", "white-glass"]`
  - **Recyclable Classes**:  
    `{"biological", "brown-glass", "cardboard", "clothes", "green-glass", "paper", "plastic", "shoes", "white-glass"}`
  - **Organic Classes**:  
    `{"biological", "paper"}`

## Instalasi

1. **Clone Repository:**
   ```
   git clone https://github.com/ZidanIndra/Flask-Deteksi-Sampah.git
   cd Flask-Deteksi-Sampah
   ```

2. **Install dependencies:**
   Gunakan `pip` untuk menginstall dependencies yang diperlukan.
   ```
   pip install -r requirements.txt
   ```

3. **Menjalankan Aplikasi:**
   Jalankan Flask server dengan perintah berikut:
   ```
   python app.py
   ```

4. **Akses Aplikasi:**
   Buka browser dan akses aplikasi di `http://127.0.0.1:5000/`.

## Model

Model yang digunakan untuk klasifikasi gambar adalah Convolutional Neural Network (CNN) yang dilatih dengan dataset sampah. Model ini di-load menggunakan format `.h5`.

## Cara Penggunaan dan Dokumentasi Website

**Halaman Utama**
![Screenshot 2024-12-25 212502](https://github.com/user-attachments/assets/53830759-9153-45f5-bdb0-e39607281808)
Halaman utama aplikasi menampilkan dua pilihan yaitu Prediksi Menggunakan Gambar dan Prediksi Secara Realtime

**Prediksi Menggunakan Gambar:** 

1. **Unggah Gambar:**
![Screenshot 2024-12-25 212550](https://github.com/user-attachments/assets/db494f45-8159-44a1-9169-42f44aa6448a)
   - Pilih gambar sampah yang ingin diklasifikasikan.
   - Gambar yang diterima adalah format `.jpg`, `.jpeg`, atau `.png`.

3. **Hasil Klasifikasi:**
![Screenshot 2024-12-25 212653](https://github.com/user-attachments/assets/27645271-83e0-4d73-955e-e35769758820)
   - Setelah gambar diunggah, model akan mengklasifikasikan sampah ke dalam salah satu kategori di atas.
   - Sistem akan memberikan hasil kategori apakah sampah tersebut dapat didaur ulang dan apakah organik atau anorganik.


**Prediksi Secara Realtime:**

![WhatsApp Image 2024-12-25 at 21 30 19_b3a4e06d](https://github.com/user-attachments/assets/697b63d7-0a0a-4158-bc00-7204677b0365)
- Aplikasi ini dilengkapi dengan fitur deteksi real-time yang memungkinkan pengguna untuk langsung menggunakan kamera perangkat untuk memprediksi jenis sampah. Begitu pengguna mengaktifkan kamera, gambar yang diambil akan langsung diproses oleh model CNN, dan hasil klasifikasinya akan ditampilkan dalam waktu singkat di halaman yang sama
## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini dan kirimkan pull request dengan perubahan yang diinginkan.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

