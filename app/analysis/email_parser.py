import re
from typing import Dict, Any
from datetime import datetime

# parse email to extract basic fields
def parse_email(subject: str, body: str, sender: str) -> Dict[str, Any]:

    subject = subject or ""
    body = body or ""
    sender = sender or ""
    
    return {
        "subject": subject,
        "body": body[:500],
        "sender": sender,
        "subject_length": len(subject),
        "body_length": len(body),
        "parsed_at": datetime.utcnow().isoformat()
    }