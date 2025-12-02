import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

X = [
    "Congratulations, you won a prize!",
    "Your account has been hacked, click here",
    "Hello, how are you?",
    "Meeting tomorrow at 10am",
    "Verify your login to avoid suspension"
]

y = [1, 1, 0, 0, 1]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

os.makedirs("../model", exist_ok=True)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("[+] Model și vectorizer salvați în folderul model/")
