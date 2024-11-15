from flask import Flask, render_template, request, Response, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import os

app = Flask(__name__)

# Load model CNN
model_path = 'model\predictWaste12.h5'
model = load_model(model_path)

output_class = ["battery", "biological", "brown-glass", "cardboard", "clothes",
                "green-glass", "metal", "paper", "plastic", "shoes", "trash", "white-glass"]

recyclable_classes = {"biological", "brown-glass", "cardboard", "clothes",
                      "green-glass", "paper", "plastic", "shoes", "white-glass"}

organic_classes = {"biological", "paper"}

# Fungsi prediksi gambar dari file
def classify_image(file_path):
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediksi menggunakan model
    predicted_array = model.predict(img_array)
    class_index = np.argmax(predicted_array)
    predicted_value = output_class[class_index]
    predicted_accuracy = round(np.max(predicted_array) * 100, 2)

    # Tentukan kategori daur ulang dan organik/anorganik
    recycle_status = "Bisa didaur ulang" if predicted_value in recyclable_classes else "Tidak bisa didaur ulang"
    organic_status = "Organik" if predicted_value in organic_classes else "Anorganik"

    return predicted_value, predicted_accuracy, recycle_status, organic_status

# Fungsi prediksi dari kamera
def classify_frame(frame):
    img = cv2.resize(frame, (224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predicted_array = model.predict(img_array)
    class_index = np.argmax(predicted_array)
    predicted_value = output_class[class_index]
    predicted_accuracy = round(np.max(predicted_array) * 100, 2)

    recycle_status = "Bisa didaur ulang" if predicted_value in recyclable_classes else "Tidak bisa didaur ulang"
    organic_status = "Organik" if predicted_value in organic_classes else "Anorganik"

    return predicted_value, predicted_accuracy, recycle_status, organic_status

@app.route('/')
def index():
    return render_template('index.html')

# Route untuk upload gambar dan klasifikasi
@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img_path = os.path.join('static', 'uploads', file.filename)
            file.save(img_path)
            label, accuracy, recycle_status, organic_status = classify_image(img_path)
            return render_template('result.html', label=label, accuracy=accuracy, recycle_status=recycle_status, organic_status=organic_status, img_path=img_path)
    return render_template('upload.html')

# Generator untuk video streaming dari kamera
def generate_frames():
    cap = cv2.VideoCapture(0)

    # Tentukan ukuran dan posisi kotak prediksi
    box_size = 224  # Sesuaikan dengan ukuran input model
    frame_center = (320, 240)  # Asumsi resolusi kamera adalah 640x480
    top_left = (frame_center[0] - box_size // 2, frame_center[1] - box_size // 2)
    bottom_right = (frame_center[0] + box_size // 2, frame_center[1] + box_size // 2)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Buat salinan area yang di dalam kotak untuk klasifikasi
            roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            if roi.shape[0] == box_size and roi.shape[1] == box_size:
                label, accuracy, recycle_status, organic_status = classify_frame(roi)
                text = f"{label} ({accuracy}%) - {recycle_status} - {organic_status}"

                # Tambahkan teks hasil prediksi di atas kotak
                cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Gambar kotak di tengah frame
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

            # Encode frame untuk streaming
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route untuk video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route untuk halaman streaming kamera
@app.route('/real_time')
def real_time():
    return render_template('real_time.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
