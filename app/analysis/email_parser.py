import re

def extract_email_features(email_text, sender=""):
    links = re.findall(r"https?://\S+", email_text)
    keywords = ["verify", "login", "prize", "suspend"]
    keyword_count = sum(email_text.lower().count(k) for k in keywords)
    return {
        "num_links": len(links),
        "keyword_count": keyword_count,
        "sender_present": 1 if sender else 0
    }
