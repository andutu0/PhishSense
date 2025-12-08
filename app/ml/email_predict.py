from app.ml.email_model_loader import email_model, email_vectorizer
import numpy as np

# predict if an email is phishing or benign
def predict_email(subject: str, body: str, sender: str) -> dict:
    # combine email components into single text for analysis
    combined_text = f"{subject} {body} {sender}".strip()
    
    if not combined_text:
        return {
            "verdict": "benign",
            "confidence": 0.0,
            "error": "Empty email content"
        }
    
    # transform text using vectorizer
    text_features = email_vectorizer.transform([combined_text])
    
    # get prediction
    prediction = email_model.predict(text_features)[0]
    
    # get probability scores
    proba = email_model.predict_proba(text_features)[0]
    
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
        "subject": subject,
        "body": body[:100], # truncate for logging
        "sender": sender
    }