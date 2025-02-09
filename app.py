from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Menambahkan CORS untuk mengizinkan permintaan dari domain lain

# API untuk menghapus background
@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Buka gambar dan proses dengan rembg
    image = Image.open(file)
    output = remove(image)

    # Simpan hasil ke buffer
    img_io = io.BytesIO()
    output.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # CORS untuk semua origin
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Metode yang diizinkan
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')  # Header yang diizinkan
    return response

