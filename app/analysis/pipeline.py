from datetime import datetime
from typing import Dict, Any, List

from app.analysis import url_utils, feature_extractor
from app.analysis import email_parser, qr_parser
from app.ml import predict as ml_predict


PHISHING_THRESHOLD = 0.5


def _timestamp() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _classify_url(url: str) -> Dict[str, Any]:
    parsed = url_utils.extract_url_features(url)
    feats = feature_extractor.build_features_from_url(parsed)
    score = ml_predict.predict_proba(feats)
    verdict = "suspicious" if score >= PHISHING_THRESHOLD else "safe"

    return {
        "type": "url",
        "input": parsed["normalized_url"],
        "verdict": verdict,
        "score": score,
        "indicators": parsed,
        "timestamp": _timestamp(),
    }


def analyze_url(url: str) -> Dict[str, Any]:
    url = (url or "").strip()
    if not url:
        return {
            "type": "url",
            "input": url,
            "verdict": "invalid",
            "score": 0.0,
            "indicators": {"reason": "empty url"},
            "timestamp": _timestamp(),
        }
    return _classify_url(url)


def analyze_email(subject: str, body: str, sender: str) -> Dict[str, Any]:
    parsed = email_parser.analyze_email(subject, body, sender)

    url_results: List[Dict[str, Any]] = []
    for url in parsed["urls"]:
        url_results.append(_classify_url(url))

    worst_score = max((r["score"] for r in url_results), default=0.0)
    suspicious_by_urls = worst_score >= PHISHING_THRESHOLD

    phishing_phrase_hits = parsed.get("phishing_phrase_hits", 0)
    suspicious_by_phrases = phishing_phrase_hits > 0

    verdict = "suspicious" if (suspicious_by_urls or suspicious_by_phrases) else "safe"

    return {
        "type": "email",
        "input": {
            "subject": subject,
            "sender": sender,
            "num_urls": parsed["num_urls"],
        },
        "verdict": verdict,
        "score": worst_score,
        "indicators": {
            "sender_domain": parsed["sender_domain"],
            "urls": [r["input"] for r in url_results],
            "url_results": url_results,
            "phishing_phrase_hits": phishing_phrase_hits,
            "phishing_phrase_count_in_dataset": parsed.get(
                "phishing_phrase_count_in_dataset", 0
            ),
        },
        "timestamp": _timestamp(),
    }


def analyze_qr_image(file_storage) -> Dict[str, Any]:
    decoded = qr_parser.decode_qr_image(file_storage)
    data = decoded["raw_data"]

    if decoded["type"] == "url" and data:
        url_result = _classify_url(data)
        verdict = url_result["verdict"]
        score = url_result["score"]
        indicators: Dict[str, Any] = {"url_result": url_result}
    else:
        verdict = "unknown"
        score = 0.0
        indicators = decoded

    return {
        "type": "qr",
        "input": data,
        "verdict": verdict,
        "score": score,
        "indicators": indicators,
        "timestamp": _timestamp(),
    }
