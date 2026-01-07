from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os


app = Flask(__name__)
CORS(app)  


# ============================
# EDGE DETECTION FUNCTION
# ============================
def edge_detection(img, method):
    if img is None:
        raise ValueError("Gambar tidak valid")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # =======================
    # SOBEL
    # =======================
    if method == "sobel":
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        edge = cv2.magnitude(gx, gy)

    # =======================
    # PREWITT
    # =======================
    elif method == "prewitt":
        kx = np.array([[1, 0, -1],
                       [1, 0, -1],
                       [1, 0, -1]], dtype=np.float32)

        ky = np.array([[1, 1, 1],
                       [0, 0, 0],
                       [-1, -1, -1]], dtype=np.float32)

        gx = cv2.filter2D(gray, cv2.CV_64F, kx)
        gy = cv2.filter2D(gray, cv2.CV_64F, ky)
        edge = cv2.magnitude(gx, gy)

    # =======================
    # LAPLACE
    # =======================
    elif method == "laplace":
        edge = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
        edge = np.abs(edge)

    # =======================
    # FREI-CHEN
    # =======================
    elif method == "freichen":
        k1 = np.array([[1, np.sqrt(2), 1],
                       [0, 0, 0],
                       [-1, -np.sqrt(2), -1]], dtype=np.float32)

        k2 = np.array([[1, 0, -1],
                       [np.sqrt(2), 0, -np.sqrt(2)],
                       [1, 0, -1]], dtype=np.float32)

        gx = cv2.filter2D(gray, cv2.CV_64F, k1)
        gy = cv2.filter2D(gray, cv2.CV_64F, k2)
        edge = cv2.magnitude(gx, gy)

    # =======================
    # ROBERTS
    # =======================
    elif method == "roberts":
        kx = np.array([[1, 0],
                       [0, -1]], dtype=np.float32)

        ky = np.array([[0, 1],
                       [-1, 0]], dtype=np.float32)

        gx = cv2.filter2D(gray, cv2.CV_64F, kx)
        gy = cv2.filter2D(gray, cv2.CV_64F, ky)
        edge = cv2.magnitude(gx, gy)

    else:
        raise ValueError("Metode tidak dikenali")

    # =======================
    # NORMALIZATION
    # =======================
    edge = cv2.normalize(edge, None, 0, 255, cv2.NORM_MINMAX)
    return edge.astype(np.uint8)


# ============================
# API ENDPOINT
# ============================
@app.route("/process", methods=["POST"])
def process_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "File gambar tidak ditemukan"}), 400

        file = request.files["image"]
        method = request.form.get("method", "")

        if method == "":
            return jsonify({"error": "Metode belum dipilih"}), 400

        img_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        result = edge_detection(img, method)

        _, buffer = cv2.imencode(".png", result)
        encoded = base64.b64encode(buffer).decode("utf-8")

        return jsonify({"image": encoded})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================
# RUN SERVER
# ============================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

