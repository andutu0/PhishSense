from .url_utils import extract_url_features
from .email_parser import extract_email_features
from .feature_extractor import extract_features_text
from app.ml.predict import predict

from .qr_parser import decode_qr
import io

def analyze_url(url):
    features = extract_url_features(url)
    vector_text = str(features)
    result = predict(vector_text)
    return result

def analyze_email(text, sender=None):
    features = extract_email_features(text, sender=sender)
    vector_text = str(features)
    result = predict(vector_text)
    return result

def analyze_qr_image(file_obj):
    try:
        text = decode_qr(file_obj)
        if not text:
            return {"verdict": "safe", "confidence": 0.5}
        if text.startswith("http://") or text.startswith("https://"):
            result = analyze_url(text)
        else:
            result = analyze_email(text)
        return result
    except Exception as e:
        print("[!] Error decoding QR:", e)
        return {"verdict": "safe", "confidence": 0.5}
