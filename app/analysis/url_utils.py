import re
from urllib.parse import urlparse
from typing import Dict, Any

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "confirm",
]

SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
}


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return url
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url
    return url


def is_ip_address(host: str) -> bool:
    return bool(re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host))


def extract_url_features(url: str) -> Dict[str, Any]:
    normalized = normalize_url(url)
    parsed = urlparse(normalized)

    host = parsed.netloc.lower()
    path = parsed.path or "/"
    full = normalized.lower()

    num_dots = host.count(".")
    num_digits = sum(ch.isdigit() for ch in host + path)
    has_at = "@" in full
    has_https = parsed.scheme == "https"
    url_length = len(full)

    suspicious_words = sum(1 for w in SUSPICIOUS_WORDS if w in full)
    host_no_port = host.split(":")[0] if host else ""
    is_shortener = host_no_port in SHORTENER_DOMAINS
    uses_ip = is_ip_address(host_no_port) if host_no_port else False

    return {
        "raw_url": url,
        "normalized_url": normalized,
        "scheme": parsed.scheme,
        "host": host_no_port,
        "path": path,
        "url_length": url_length,
        "num_dots": num_dots,
        "num_digits": num_digits,
        "has_at_symbol": int(has_at),
        "has_https": int(has_https),
        "suspicious_word_count": suspicious_words,
        "is_shortener": int(is_shortener),
        "uses_ip": int(uses_ip),
    }
