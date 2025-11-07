from flask import Blueprint, render_template, request, jsonify
from .model import predict
from .qr_utils import decode_qr

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/analyze", methods=["POST"])
def analyze():
    text_input = ""

    # Handle QR image upload
    if "qr_file" in request.files and request.files["qr_file"].filename != "":
        qr_file = request.files["qr_file"]
        text_input = decode_qr(qr_file)
    else:
        text_input = request.form.get("text", "")

    if not text_input.strip():
        return jsonify({"error": "No input provided"}), 400

    result = predict(text_input)
    return jsonify(result)
