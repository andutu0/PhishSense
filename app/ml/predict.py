from .model_loader import get_model
import numpy as np

def predict(text):
    model, vectorizer = get_model()
    if model is None or vectorizer is None:
        return {"verdict": "safe", "confidence": 0.5}

    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0, 1]
    verdict = "malicious" if prob > 0.5 else "safe"
    return {"verdict": verdict, "confidence": float(round(prob, 3))}
