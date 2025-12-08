import re
from urllib.parse import urlparse
from typing import Dict, Any
import pandas as pd
from pathlib import Path

# load suspicious words from email_dataset.csv
def load_suspicious_words():
    try:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
        email_data_path = PROJECT_ROOT / "data" / "email_dataset.csv"
        
        if email_data_path.exists():
            df = pd.read_csv(email_data_path)
            # get all phishing phrases and extract individual words
            phishing_phrases = df[df['label'] == 'phishing']['phrase'].tolist()
            
            # extract unique words from phrases
            suspicious_words = set()
            for phrase in phishing_phrases:
                # split phrase into words and add to set
                words = phrase.lower().split()
                suspicious_words.update(words)
            
            return list(suspicious_words)
        else:
            # fallback list if file not found
            return [
                "login", "verify", "update", "secure", "account", 
                "bank", "confirm", "urgent", "suspended", "click",
                "password", "billing", "prize", "won", "winner"
            ]
    except Exception as e:
        print(f"Error loading suspicious words: {e}")
        return [
            "login", "verify", "update", "secure", "account", 
            "bank", "confirm", "urgent", "suspended", "click"
        ]

# load suspicious words from dataset
SUSPICIOUS_WORDS = load_suspicious_words()

# common URL shortening service domains
SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
}

# normalize URL by ensuring it has a scheme
def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return url
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url
    return url

# check if host is an IP address
def is_ip_address(host: str) -> bool:
    return bool(re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host))

# extract various features from the URL
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