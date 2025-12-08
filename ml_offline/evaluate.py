import argparse
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple

from sklearn.metrics import classification_report

from app.analysis import url_utils, feature_extractor
from app.ml.model_loader import get_model_and_vectorizer

# load dataset from CSV
def load_dataset(csv_path: Path) -> Tuple[List[Dict[str, Any]], List[int]]:
    feats: List[Dict[str, Any]] = []
    labels: List[int] = []

    with csv_path.open("r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row["url"]
            label_raw = str(row["label"]).strip().lower()

            if label_raw in ("phish", "phishing", "malicious", "bad", "1"):
                label = 1
            else:
                label = 0

            parsed = url_utils.extract_url_features(url)
            feat = feature_extractor.build_features_from_url(parsed)
            feats.append(feat)
            labels.append(label)

    return feats, labels

# main evaluation function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to CSV dataset")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    X_dicts, y_true = load_dataset(csv_path)

    model, vec = get_model_and_vectorizer()
    X = vec.transform(X_dicts)
    y_pred = model.predict(X)

    print(classification_report(y_true, y_pred))


if __name__ == "__main__":
    main()
