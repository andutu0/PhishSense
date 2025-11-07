# save_dummy_model.py
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

X = ["hello world", "your account has been compromised, click here", "urgent verify now"]
y = [0, 1, 1]

vec = TfidfVectorizer()
X_vec = vec.fit_transform(X)
model = LogisticRegression().fit(X_vec, y)

joblib.dump(model, "model/model.joblib")
joblib.dump(vec, "model/vectorizer.joblib")

print("Dummy model saved ✅")
