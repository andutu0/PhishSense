from typing import Dict, Any

from app.ml.model_loader import get_model_and_vectorizer


def predict_proba(feature_dict: Dict[str, Any]) -> float:
    model, vectorizer = get_model_and_vectorizer()
    X = vectorizer.transform([feature_dict])
    proba = model.predict_proba(X)[0][1]
    return float(proba)


def predict_label(feature_dict: Dict[str, Any], threshold: float = 0.5) -> int:
    score = predict_proba(feature_dict)
    return int(score >= threshold)
