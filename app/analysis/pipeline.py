from typing import Dict, Any
from datetime import datetime, timezone

from app.analysis import email_parser, qr_parser, url_utils

# analyze a URL and return the result
def analyze_url(url: str) -> dict:
    # import here to avoid circular imports
    from app.ml.predict import predict_url
    
    # extract URL features
    indicators = url_utils.extract_url_features(url)
    result = predict_url(url)
    
    # get verdict and confidence from model result
    verdict = result.get('verdict', 'benign')
    confidence = result.get('confidence', 0)
    
    return {
        "type": "url",
        "input": url,
        "verdict": verdict,
        "score": confidence,
        "confidence": confidence,
        "indicators": indicators,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# analyze an email and return the result
def analyze_email(subject: str, body: str, sender: str) -> dict:
    from app.ml.email_predict import predict_email
    
    # extract email features
    parsed = email_parser.parse_email(subject, body, sender)
    result = predict_email(subject, body, sender)
    
    # get verdict and confidence from model result
    verdict = result.get('verdict', 'benign')
    confidence = result.get('confidence', 0)
    
    return {
        "type": "email",
        "verdict": verdict,
        "score": confidence,
        "confidence": confidence,
        "parsed": parsed,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# analyze a QR code image and return the result
def analyze_qr_image(file) -> dict:
    decoded_data = qr_parser.decode_qr_from_file(file)
    # extract QR code data
    if not decoded_data:
        return {
            "type": "qr",
            "verdict": "error",
            "score": 0.0,
            "confidence": 0.0,
            "error": "No QR code detected in image",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    # determine if decoded data is a URL or email content
    if decoded_data.startswith("http://") or decoded_data.startswith("https://"):
        return analyze_url(decoded_data)
    else:
        return analyze_email("", decoded_data, "")