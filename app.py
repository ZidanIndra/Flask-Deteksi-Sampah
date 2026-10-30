from flask import Flask, render_template, request, Response, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import os
import time
import base64

app = Flask(__name__)

# Base directory & model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'predictWaste12.h5')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model CNN
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print(f"[OK] Model loaded: {MODEL_PATH}")
    else:
        print(f"[WARN] Model file not found at: {MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")

output_class = ["battery", "biological", "brown-glass", "cardboard", "clothes",
                "green-glass", "metal", "paper", "plastic", "shoes", "trash", "white-glass"]

recyclable_classes = {"biological", "brown-glass", "cardboard", "clothes",
                      "green-glass", "paper", "plastic", "shoes", "white-glass"}

organic_classes = {"biological", "paper"}

# Detailed metadata for each class
CATEGORY_METADATA = {
    "battery": {
        "id_name": "Baterai (Limbah B3)",
        "en_name": "Battery",
        "recycle_status": "Tidak bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": False,
        "is_organic": False,
        "color": "amber",
        "icon": "fa-car-battery",
        "tip": "Baterai mengandung logam berat & bahan kimia berbahaya. Jangan dibuang ke tempat sampah biasa atau dibakar. Serahkan ke drop box e-waste atau bank sampah B3."
    },
    "biological": {
        "id_name": "Sampah Biologis / Makanan",
        "en_name": "Biological",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Organik",
        "is_recyclable": True,
        "is_organic": True,
        "color": "emerald",
        "icon": "fa-apple-whole",
        "tip": "Sisa makanan dan daun dapat diolah menjadi pupuk kompos bernutrisi tinggi atau pakan maggot BSF untuk budidaya ramah lingkungan."
    },
    "brown-glass": {
        "id_name": "Kaca Cokelat",
        "en_name": "Brown Glass",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "amber",
        "icon": "fa-wine-bottle",
        "tip": "Kaca cokelat dapat didaur ulang tanpa batas tanpa menurunkan kualitas. Bilas sisa cairan, lepas tutup botol, dan pisahkan dari kaca bening."
    },
    "cardboard": {
        "id_name": "Kardus / Karton",
        "en_name": "Cardboard",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "yellow",
        "icon": "fa-box-open",
        "tip": "Lipat kardus hingga pipih untuk menghemat ruang penyimpanan. Pastikan kardus dalam keadaan kering dan bebas dari noda minyak atau lem basah."
    },
    "clothes": {
        "id_name": "Pakaian / Tekstil",
        "en_name": "Clothes / Textile",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "indigo",
        "icon": "fa-shirt",
        "tip": "Pakaian layak pakai sebaiknya didonasikan. Pakaian rusak dapat disalurkan ke program daur ulang serat tekstil atau dimanfaatkan kembali sebagai lap serbaguna."
    },
    "green-glass": {
        "id_name": "Kaca Hijau",
        "en_name": "Green Glass",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "emerald",
        "icon": "fa-wine-bottle",
        "tip": "Kaca hijau dapat didaur ulang 100%. Bilas bersih dari sisa isi minuman sebelum disetorkan ke bank sampah atau tempat daur ulang kaca."
    },
    "metal": {
        "id_name": "Logam / Kaleng",
        "en_name": "Metal / Can",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "slate",
        "icon": "fa-cubes-stacked",
        "tip": "Kaleng minuman atau kaleng makanan memiliki nilai ekonomi tinggi untuk didaur ulang. Cuci bersih dan tekan/pipihkan untuk menghemat tempat."
    },
    "paper": {
        "id_name": "Kertas",
        "en_name": "Paper",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Organik",
        "is_recyclable": True,
        "is_organic": True,
        "color": "blue",
        "icon": "fa-newspaper",
        "tip": "Kertas bekas dan kardus dapat didaur ulang menjadi kertas baru. Kumpulkan dalam kondisi kering, hindari terkena minyak atau cairan kimia."
    },
    "plastic": {
        "id_name": "Plastik",
        "en_name": "Plastic",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "cyan",
        "icon": "fa-bottle-water",
        "tip": "Pisahkan tutup botol dan label plastik jika jenisnya berbeda. Bilas botol hingga bersih dari sisa cairan manis dan remas botol untuk menghemat volume."
    },
    "shoes": {
        "id_name": "Sepatu / Alas Kaki",
        "en_name": "Shoes",
        "recycle_status": "Tidak bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": False,
        "is_organic": False,
        "color": "purple",
        "icon": "fa-shoe-prints",
        "tip": "Sepatu terdiri dari kombinasi berbagai material sintetis, karet, dan lem yang sulit didaur ulang secara umum. Jika masih layak, donasikan kepada yang membutuhkan."
    },
    "trash": {
        "id_name": "Sampah Residu Umum",
        "en_name": "General Trash",
        "recycle_status": "Tidak bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": False,
        "is_organic": False,
        "color": "rose",
        "icon": "fa-trash-can",
        "tip": "Sampah residu yang tidak bisa didaur ulang atau dikompos. Bungkus rapat dan buang ke tong sampah residu (warna abu-abu/hitam) menuju TPA."
    },
    "white-glass": {
        "id_name": "Kaca Bening",
        "en_name": "White / Clear Glass",
        "recycle_status": "Bisa didaur ulang",
        "organic_status": "Anorganik",
        "is_recyclable": True,
        "is_organic": False,
        "color": "teal",
        "icon": "fa-glass-water",
        "tip": "Kaca bening memiliki kemurnian tinggi dalam proses daur ulang. Bersihkan dari sisa cairan dan bungkus bagian tajam jika terdapat pecahan."
    }
}

CONFIDENCE_THRESHOLD = 70.0

def validate_waste_image(pil_img):
    """Filter pengaman kualitas gambar dasar (gelap total, silau ekstrem, polos tanpa objek)"""
    gray = pil_img.convert('L').resize((100, 100))
    arr = np.array(gray, dtype=np.float32)
    mean_val = float(np.mean(arr))
    std_val = float(np.std(arr))
    
    if mean_val < 25.0:
        return False, "Gambar terlalu gelap atau minim pencahayaan."
    if mean_val > 245.0:
        return False, "Gambar terlalu silau / overexposure."
    if std_val < 18.0:
        return False, "Gambar tidak memuat objek kontras (background kosong)."
    return True, None

def check_human_face(pil_img):
    """Deteksi wajah manusia menggunakan Haar Cascade dan analisis biometrik kulit/rambut"""
    try:
        np_rgb = np.array(pil_img.convert('RGB'))
        h, w, _ = np_rgb.shape

        # 1. Haar Cascade Frontal & Profile Face Detection
        if cv2 is not None and hasattr(cv2, 'data') and hasattr(cv2.data, 'haarcascades'):
            np_gray = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2GRAY)
            for cascade_name in ['haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml']:
                p = os.path.join(cv2.data.haarcascades, cascade_name)
                if os.path.exists(p):
                    casc = cv2.CascadeClassifier(p)
                    if not casc.empty():
                        detected = casc.detectMultiScale(np_gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
                        if len(detected) > 0:
                            return True

        # 2. Analisis Biometrik Kulit (YCbCr) & Rambut
        if cv2 is not None:
            ycrcb = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2YCrCb)
            lower_skin = np.array([0, 133, 77], dtype=np.uint8)
            upper_skin = np.array([255, 173, 127], dtype=np.uint8)
            skin_mask = cv2.inRange(ycrcb, lower_skin, upper_skin)
            skin_ratio = np.count_nonzero(skin_mask) / (h * w)

            top_h = max(1, int(h * 0.35))
            top_slice = np_rgb[:top_h, :]
            dark_hair = np.count_nonzero(np.all(top_slice < 60, axis=-1)) / (top_h * w)
            top_lum = np.mean(top_slice)
            mid_lum = np.mean(np_rgb[top_h:int(h * 0.70), :])

            if (skin_ratio > 0.18 and dark_hair > 0.05 and (mid_lum - top_lum) > 15) or (skin_ratio > 0.38):
                return True
    except Exception:
        pass
    return False

def predict_from_pil(pil_img):
    """Prediksi array gambar PIL ke 12 kelas sampah dengan pengaman OOD"""
    if model is None:
        raise RuntimeError("Model CNN belum dimuat atau file model tidak ditemukan.")

    # 1. Validasi fisik gambar
    is_img_valid, img_err = validate_waste_image(pil_img)

    # 2. Validasi wajah manusia
    is_face = check_human_face(pil_img)

    img = pil_img.convert('RGB').resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predicted_array = model.predict(img_array)
    class_index = int(np.argmax(predicted_array))
    predicted_value = output_class[class_index]
    predicted_accuracy = round(float(np.max(predicted_array)) * 100, 2)

    # 3. Evaluasi ambang batas keamanan (Safety Guard)
    if is_face:
        is_valid = False
        error_message = "Objek tidak valid: Terdeteksi wajah manusia, bukan objek sampah."
    elif not is_img_valid:
        is_valid = False
        error_message = f"Objek tidak valid: {img_err}"
    elif predicted_accuracy < CONFIDENCE_THRESHOLD:
        is_valid = False
        error_message = f"Objek tidak dikenali sebagai sampah (keyakinan {predicted_accuracy}% di bawah ambang aman 70%)."
    else:
        is_valid = True
        error_message = None

    meta = CATEGORY_METADATA.get(predicted_value, {
        "id_name": predicted_value.capitalize(),
        "en_name": predicted_value.capitalize(),
        "recycle_status": "Bisa didaur ulang" if predicted_value in recyclable_classes else "Tidak bisa didaur ulang",
        "organic_status": "Organik" if predicted_value in organic_classes else "Anorganik",
        "is_recyclable": predicted_value in recyclable_classes,
        "is_organic": predicted_value in organic_classes,
        "color": "emerald" if predicted_value in recyclable_classes else "rose",
        "icon": "fa-recycle",
        "tip": "Pilah sampah dengan benar sesuai petunjuk pengelolaan sampah lingkungan."
    })

    return {
        "is_valid": is_valid,
        "error_message": error_message,
        "label": predicted_value if is_valid else "invalid",
        "id_name": meta["id_name"] if is_valid else "Objek Tidak Valid",
        "en_name": meta["en_name"] if is_valid else "Invalid Non-Waste",
        "accuracy": predicted_accuracy,
        "recycle_status": meta["recycle_status"] if is_valid else "Tidak Teridentifikasi",
        "organic_status": meta["organic_status"] if is_valid else "Bukan Sampah",
        "is_recyclable": meta["is_recyclable"] if is_valid else False,
        "is_organic": meta["is_organic"] if is_valid else False,
        "color": meta["color"] if is_valid else "rose",
        "icon": meta["icon"] if is_valid else "fa-triangle-exclamation",
        "tip": meta["tip"] if is_valid else "Arahkan kamera atau unggah foto yang fokus pada objek sampah spesifik (plastik, kertas, kaleng, kardus, botol kaca, dll)."
    }

def classify_image(file_path):
    with Image.open(file_path) as img:
        res = predict_from_pil(img)
    return res["label"], res["accuracy"], res["recycle_status"], res["organic_status"], res

def classify_frame(frame):
    # Convert BGR frame from OpenCV to RGB PIL Image
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_frame)
    res = predict_from_pil(pil_img)
    return res["label"], res["accuracy"], res["recycle_status"], res["organic_status"]

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORY_METADATA)

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                ext = '.jpg'
            
            clean_name = secure_filename(file.filename) or "upload.jpg"
            filename = f"scan_{int(time.time())}_{clean_name}"
            if not filename.endswith(ext):
                filename += ext

            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)

            try:
                label, accuracy, recycle_status, organic_status, res = classify_image(img_path)
                web_img_path = url_for('static', filename=f'uploads/{filename}')

                return render_template(
                    'result.html',
                    is_valid=res.get('is_valid', True),
                    error_message=res.get('error_message'),
                    label=label,
                    accuracy=accuracy,
                    recycle_status=recycle_status,
                    organic_status=organic_status,
                    id_name=res['id_name'],
                    en_name=res['en_name'],
                    is_recyclable=res['is_recyclable'],
                    is_organic=res['is_organic'],
                    color=res['color'],
                    icon=res['icon'],
                    tip=res['tip'],
                    img_path=web_img_path
                )
            except Exception as e:
                return render_template('upload.html', error=f"Gagal memproses gambar: {str(e)}")

    return render_template('upload.html')

@app.route('/api/classify', methods=['POST'])
def api_classify():
    """Endpoint API untuk klasifikasi real-time dari kamera browser atau AJAX"""
    try:
        # Pilihan 1: File multipart
        if 'file' in request.files:
            file = request.files['file']
            if not file or file.filename == '':
                return jsonify({'success': False, 'error': 'Tidak ada berkas yang dikirim'}), 400
            with Image.open(file.stream) as img:
                res = predict_from_pil(img)
            return jsonify({'success': True, **res})

        # Pilihan 2: Base64 JSON image dari Canvas Webcam
        data = request.get_json(silent=True)
        if data and 'image' in data:
            image_b64 = data['image']
            if ',' in image_b64:
                image_b64 = image_b64.split(',', 1)[1]
            img_bytes = base64.b64decode(image_b64)
            with Image.open(BytesIO(img_bytes)) as img:
                res = predict_from_pil(img)
            return jsonify({'success': True, **res})

        return jsonify({'success': False, 'error': 'Data gambar tidak ditemukan'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_frames():
    cap = cv2.VideoCapture(0)
    box_size = 224
    frame_center = (320, 240)
    top_left = (frame_center[0] - box_size // 2, frame_center[1] - box_size // 2)
    bottom_right = (frame_center[0] + box_size // 2, frame_center[1] + box_size // 2)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            if roi.shape[0] == box_size and roi.shape[1] == box_size:
                try:
                    label, accuracy, recycle_status, organic_status = classify_frame(roi)
                    text = f"{label} ({accuracy}%) - {recycle_status}"
                    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                except Exception:
                    pass

            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/real_time')
def real_time():
    return render_template('real_time.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)
