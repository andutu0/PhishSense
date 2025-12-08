import json
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(exist_ok=True)
LOG_PATH = DATA_DIR / "scans.jsonl"
SESSION_LOG_PATH = DATA_DIR / "session_scans.jsonl"
SESSION_ID = uuid.uuid4().hex


def append_scan(record: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Persist scan to global log and current session log."""
    DATA_DIR.mkdir(exist_ok=True)
    
    sid = session_id or SESSION_ID
    entry = dict(record)
    entry.setdefault("session_id", sid)
    
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    
    with LOG_PATH.open("a", encoding="utf8") as f:
        f.write(line)
    
    with SESSION_LOG_PATH.open("a", encoding="utf8") as f:
        f.write(line)
    
    return sid


def get_recent_scans(limit: int = 20) -> List[Dict[str, Any]]:
    if not LOG_PATH.exists():
        return []

    with LOG_PATH.open("r", encoding="utf8") as f:
        lines = f.readlines()

    selected = lines[-limit:]
    records: List[Dict[str, Any]] = []

    for line in selected:
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return records


def get_session_scans(session_id: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Return scans from the current session (or specified session_id)."""
    if not SESSION_LOG_PATH.exists():
        return []
    
    sid = session_id or SESSION_ID
    
    with SESSION_LOG_PATH.open("r", encoding="utf8") as f:
        lines = f.readlines()
    
    records: List[Dict[str, Any]] = []
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        if rec.get("session_id") != sid:
            continue
        
        records.append(rec)
        if len(records) >= limit:
            break
    
    return list(reversed(records))

