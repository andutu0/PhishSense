import joblib
from pathlib import Path

# get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "model"

# load the URL classification model and vectorizer
def load_url_model():
    model_path = MODEL_DIR / "model.joblib"
    vectorizer_path = MODEL_DIR / "vectorizer.joblib"
    
    if not model_path.exists() or not vectorizer_path.exists():
        raise FileNotFoundError(
            f"URL model files not found. Please run: python3 ml_offline/train.py"
        )
    
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    return model, vectorizer

# load once at module import
url_model, url_vectorizer = load_url_model()