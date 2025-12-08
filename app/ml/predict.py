from app.ml.model_loader import url_model, url_vectorizer

# predict if a URL is phishing or benign
def predict_url(url: str) -> dict:
    if not url:
        return {
            "verdict": "benign",
            "confidence": 0.0,
            "error": "Empty URL"
        }
    
    # transform URL using vectorizer
    url_features = url_vectorizer.transform([url])
    
    # get prediction
    prediction = url_model.predict(url_features)[0]
    
    # get probability scores
    proba = url_model.predict_proba(url_features)[0]
    
    # determine verdict and confidence
    if prediction == 1 or prediction == "phishing":
        verdict = "phishing"
        confidence = proba[1] if len(proba) > 1 else proba[0]
    else:
        verdict = "benign"
        confidence = proba[0] if len(proba) > 1 else proba[0]
    
    return {
        "verdict": verdict,
        "confidence": float(confidence),
        "score": float(proba[1] if len(proba) > 1 else confidence),
        "url": url
    }