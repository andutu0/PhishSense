import joblib
import numpy as np

model = None
vectorizer = None

# load model and vectorizer
def load_model(model_path, vectorizer_path):
    global model, vectorizer
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        print("[+] Model and vectorizer loaded.")
    except Exception as e:
        print("[!] Could not load model/vectorizer:", e)
        model = None
        vectorizer = None

# predict function
def predict(text):
    if model is None or vectorizer is None:
        return {"verdict": "safe", "confidence": 0.5}

    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0, 1]
    verdict = "malicious" if prob > 0.5 else "safe"
    return {"verdict": verdict, "confidence": float(round(prob, 3))}
