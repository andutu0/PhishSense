import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(exist_ok=True)
LOG_PATH = DATA_DIR / "scans.jsonl"


def append_scan(record: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


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
