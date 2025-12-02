import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# --- Încarcă model și vectorizer ---
model_path = "model.pkl"
vectorizer_path = "vectorizer.pkl"

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("[+] Model și vectorizer încărcate cu succes")
except Exception as e:
    print("[!] Nu s-au putut încărca modelul/vectorizerul:", e)
    exit(1)

# --- Exemplu de date de test ---
X_test = [
    "You won a free iPhone, click here",
    "Meeting at 10am tomorrow",
    "Your account is suspended, verify now",
    "Lunch at 12?",
    "Update your billing info immediately"
]

y_test = [1, 0, 1, 0, 1]  # 1 = phishing, 0 = safe

# --- Transformă textul în vectori ---
X_vec = vectorizer.transform(X_test)

# --- Prezice ---
y_pred = model.predict(X_vec)

# --- Calculează metrici ---
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n=== Metrics ===")
print(f"Accuracy : {acc:.3f}")
print(f"Precision: {prec:.3f}")
print(f"Recall   : {rec:.3f}")
print(f"F1-score : {f1:.3f}")
