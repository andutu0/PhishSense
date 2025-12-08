from typing import Dict, Any

FEATURE_KEYS = [
    "url_length",
    "num_dots",
    "num_digits",
    "has_at_symbol",
    "has_https",
    "suspicious_word_count",
    "is_shortener",
    "uses_ip",
]


def build_features_from_url(parsed: Dict[str, Any]) -> Dict[str, Any]:
    features: Dict[str, Any] = {}
    for key in FEATURE_KEYS:
        features[key] = parsed.get(key, 0)
    return features
