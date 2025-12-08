import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import List, Dict, Any, Tuple

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

from app.analysis import url_utils, feature_extractor


def load_dataset(csv_path: Path) -> Tuple[List[Dict[str, Any]], List[int]]:
    features: List[Dict[str, Any]] = []
    labels: List[int] = []

    with csv_path.open("r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "url" not in row or "label" not in row:
                continue

            url = row["url"]
            label_raw = str(row["label"]).strip().lower()

            if label_raw in ("phish", "phishing", "malicious", "bad", "1"):
                label = 1
            else:
                label = 0

            parsed = url_utils.extract_url_features(url)
            feats = feature_extractor.build_features_from_url(parsed)
            features.append(feats)
            labels.append(label)

    return features, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to CSV dataset with columns url,label",
    )
    parser.add_argument(
        "--model-dir",
        default="model",
        help="Directory to save model and vectorizer",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"Dataset file not found: {csv_path}")

    X_dicts, y = load_dataset(csv_path)

    if not X_dicts:
        raise SystemExit("Dataset is empty or could not be parsed")

    label_counts = Counter(y)
    print("Label counts:", label_counts)

    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_dicts)

    min_count = min(label_counts.values())
    num_classes = len(label_counts)
    n_samples = len(y)

    can_stratify = (
        num_classes >= 2
        and min_count >= 2
        and n_samples >= 4
    )

    if not can_stratify:
        print()
        print("Warning: dataset too small or unbalanced for stratified train/test split.")
        print("Training on the full dataset and skipping evaluation split.")
        print()

        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, y)

    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        print()
        print("Classification report on held-out test set:")
        print(classification_report(y_test, y_pred))

    model_dir = Path(args.model_dir)
    model_dir.mkdir(exist_ok=True)

    model_path = model_dir / "model.pkl"
    vec_path = model_dir / "vectorizer.pkl"

    with model_path.open("wb") as f:
        pickle.dump(clf, f)

    with vec_path.open("wb") as f:
        pickle.dump(vec, f)

    print()
    print(f"Saved model to:      {model_path}")
    print(f"Saved vectorizer to: {vec_path}")


if __name__ == "__main__":
    main()
