import re
import csv
from pathlib import Path
from typing import List, Dict, Any

URL_PATTERN = re.compile(r"https?://[^\s]+")

EMAIL_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "email_dataset.csv"


def _load_phishing_phrases() -> List[str]:
    phrases: List[str] = []

    if not EMAIL_DATASET_PATH.exists():
        return phrases

    with EMAIL_DATASET_PATH.open("r", encoding="utf8", newline="") as f:
        reader = csv.reader(f)
        first_row = next(reader, None)

        if first_row:
            header_lower = [col.strip().lower() for col in first_row]
            is_header = False
            if len(header_lower) == 1 and header_lower[0] in {"phrase", "text", "pattern"}:
                is_header = True

            if not is_header:
                phrase = first_row[0].strip()
                if phrase:
                    phrases.append(phrase.lower())

        for row in reader:
            if not row:
                continue
            phrase = row[0].strip()
            if phrase:
                phrases.append(phrase.lower())

    return phrases


PHISHING_PHRASES: List[str] = _load_phishing_phrases()


def extract_urls_from_text(text: str) -> List[str]:
    text = text or ""
    return URL_PATTERN.findall(text)


def count_phishing_phrases(text: str) -> int:

    if not text or not PHISHING_PHRASES:
        return 0

    lower_text = text.lower()
    hits = 0
    for phrase in PHISHING_PHRASES:
        if phrase and phrase in lower_text:
            hits += 1
    return hits


def analyze_email(subject: str, body: str, sender: str) -> Dict[str, Any]:
    subject = subject or ""
    body = body or ""
    sender = sender or ""

    text = subject + "\n" + body
    urls = extract_urls_from_text(text)

    sender_domain = ""
    if "@" in sender:
        sender_domain = sender.split("@")[-1].lower()

    phishing_phrase_hits = count_phishing_phrases(text)

    return {
        "subject": subject,
        "body": body,
        "sender": sender,
        "sender_domain": sender_domain,
        "urls": urls,
        "num_urls": len(urls),
        "phishing_phrase_hits": phishing_phrase_hits,
        "phishing_phrase_count_in_dataset": len(PHISHING_PHRASES),
    }
