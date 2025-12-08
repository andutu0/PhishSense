from flask import render_template, request, jsonify, current_app
from app.analysis.pipeline import analyze_url, analyze_email, analyze_qr_image
from app.storage.json_storage import append_scan, get_recent_scans

@current_app.route('/')
def index():
    return render_template('index.html')

@current_app.route('/api/analyze_url', methods=['POST'])
def api_analyze_url():
    data = request.get_json(force=True, silent=True) or {}
    url = data.get("url", "")
    log = bool(data.get("log", False))

    result = analyze_url(url)
    if log:
        append_scan(result)
    return jsonify(result)

@current_app.route('/api/analyze_email', methods=['POST'])
def api_analyze_email():
    data = request.get_json(force=True, silent=True) or {}
    subject = data.get("subject", "")
    body = data.get("body", "")
    sender = data.get("sender", "")
    log = bool(data.get("log", False))

    result = analyze_email(subject, body, sender)
    if log:
        append_scan(result)
    return jsonify(result)

@current_app.route('/api/analyze_qr', methods=['POST'])
def api_analyze_qr():
    file = request.files.get("qr_image")
    if file is None:
        return jsonify({"error": "qr_image file is required"}), 400

    log_str = request.form.get("log", "false").lower()
    log = log_str in ("1", "true", "yes", "on")

    result = analyze_qr_image(file)
    if log:
        append_scan(result)
    return jsonify(result)

@current_app.route('/api/history', methods=['GET'])
def api_history():
    limit = request.args.get("limit", default=20, type=int)
    scans = get_recent_scans(limit=limit)
    return jsonify({"items": scans})