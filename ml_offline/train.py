#!/usr/bin/env python3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Train URL classification model")
    parser.add_argument("--csv", default="data/urls_dataset.csv", help="Path to URLs dataset")
    args = parser.parse_args()
    
    # paths
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATA_FILE = PROJECT_ROOT / args.csv
    MODEL_DIR = PROJECT_ROOT / "model"
    MODEL_DIR.mkdir(exist_ok=True)

    # load dataset
    print(f"Loading data from: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE)
    print(f"Dataset shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}")

    # prepare data
    X = df['url'].values
    y = df['label'].map({'benign': 0, 'phishing': 1}).values

    print(f"Class distribution: benign={sum(y==0)}, phishing={sum(y==1)}")

    # split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # vectorize URLs
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # train model
    print("Training model...")
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    model.fit(X_train_vec, y_train)

    # evaluate
    y_pred = model.predict(X_test_vec)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['benign', 'phishing'])}")

    # test specific URL for validating the model
    test_url = "http://paypal-dispute-resolution.org"
    test_vec = vectorizer.transform([test_url])
    test_pred = model.predict(test_vec)[0]
    test_proba = model.predict_proba(test_vec)[0]
    print(f"\nTest URL: {test_url}")
    print(f"Prediction: {'phishing' if test_pred == 1 else 'benign'}")
    print(f"Probability: {test_proba}")

    # save model
    model_path = MODEL_DIR / "model.joblib"
    vectorizer_path = MODEL_DIR / "vectorizer.joblib"
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"\nModel saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")

if __name__ == "__main__":
    main()