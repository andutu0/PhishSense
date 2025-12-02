import joblib
import os

_model = None
_vectorizer = None

def get_model(model_path="model.pkl", vectorizer_path="vectorizer.pkl"):
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        try:
            _model = joblib.load(model_path)
            _vectorizer = joblib.load(vectorizer_path)
            print("[+] Model and vectorizer loaded.")
        except Exception as e:
            print("[!] Could not load model/vectorizer:", e)
            _model, _vectorizer = None, None
    return _model, _vectorizer
