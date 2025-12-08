#!/usr/bin/env python3
import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import List, Tuple

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# load email dataset from CSV
def load_email_dataset(csv_path: Path) -> Tuple[List[str], List[int]]:
    texts: List[str] = []
    labels: List[int] = []

    with csv_path.open("r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        fieldnames = [name.strip().lower() for name in (reader.fieldnames or [])]

        if "phrase" not in fieldnames or "label" not in fieldnames:
            raise SystemExit(
                "email_dataset.csv trebuie să aibă coloanele 'phrase' și 'label'."
            )

        for row in reader:
            phrase = (row.get("phrase") or "").strip()
            if not phrase:
                continue

            raw_label = (row.get("label") or "").strip().lower()
            if raw_label in ("phish", "phishing", "spam", "malicious", "1"):
                label = 1
            else:
                # anything else is considered benign
                label = 0

            texts.append(phrase)
            labels.append(label)

    return texts, labels


def main():
    parser = argparse.ArgumentParser(
        description="Train email text model from email_dataset.csv"
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to email_dataset.csv (columns: phrase,label)",
    )
    parser.add_argument(
        "--model-dir",
        default="model",
        help="Directory to save email_model.pkl and email_vectorizer.pkl",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"Email dataset file not found: {csv_path}")

    texts, labels = load_email_dataset(csv_path)
    if not texts:
        raise SystemExit("Email dataset is empty or could not be parsed")

    label_counts = Counter(labels)
    print("Email label counts:", label_counts)

    if len(label_counts) < 2:
        raise SystemExit(
            "You have only one class in email_dataset.csv.\n"
            "Add some phrases with label 'benign' (or another label != phishing) "
            "so the model can learn the difference between phishing and non-phishing."
        )

    # vectorize email phrases
    vec = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_features=5000,
    )
    # transform text data into feature vectors
    X = vec.fit_transform(texts)

    # check if stratified split is possible
    n_samples = len(labels)
    num_classes = len(label_counts)
    min_count = min(label_counts.values())
    test_size = 0.2
    n_test = int(round(n_samples * test_size))

    can_stratify = (
        n_samples >= 10
        and num_classes >= 2
        and min_count >= 2
        and n_test >= num_classes
    )

    # train and evaluate model
    if not can_stratify:
        print()
        print(
            "Warning: email dataset too small or imbalanced for stratified train/test split."
        )
        print(
            f"n_samples={n_samples}, num_classes={num_classes}, min_count={min_count}, n_test={n_test}"
        )
        print("Training on the ENTIRE dataset and skipping test evaluation.\n")

        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, labels)
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            labels,
            test_size=test_size,
            random_state=42,
            stratify=labels,
        )

        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        print()
        print("Classification report (email model):")
        print(classification_report(y_test, y_pred))

    model_dir = Path(args.model_dir)
    model_dir.mkdir(exist_ok=True)

    email_model_path = model_dir / "email_model.pkl"
    email_vec_path = model_dir / "email_vectorizer.pkl"

    with email_model_path.open("wb") as f:
        pickle.dump(clf, f)

    with email_vec_path.open("wb") as f:
        pickle.dump(vec, f)

    print()
    print(f"Saved email model to:      {email_model_path}")
    print(f"Saved email vectorizer to: {email_vec_path}")


if __name__ == "__main__":
    main()
