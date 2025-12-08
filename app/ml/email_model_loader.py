import pickle
from pathlib import Path

# get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "model"

# load the email classification model and vectorizer
def load_email_model():
    model_path = MODEL_DIR / "email_model.pkl"
    vectorizer_path = MODEL_DIR / "email_vectorizer.pkl"
    
    if not model_path.exists() or not vectorizer_path.exists():
        raise FileNotFoundError(
            f"Email model files not found. Please run: python3 ml_offline/train_email.py --csv data/email_dataset.csv"
        )
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    return model, vectorizer

# load once at module import
email_model, email_vectorizer = load_email_model()