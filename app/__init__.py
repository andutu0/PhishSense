from flask import Flask
from .model import load_model

def create_app():
    app = Flask(__name__)

    # allow local hosts (prevents Host header 403 in newer Flask versions)
    app.config['TRUSTED_HOSTS'] = ['127.0.0.1', 'localhost', '127.0.0.1:5000', 'localhost:5000']

    app.config["MODEL_PATH"] = "model/model.joblib"
    app.config["VECTORIZER_PATH"] = "model/vectorizer.joblib"

    load_model(app.config["MODEL_PATH"], app.config["VECTORIZER_PATH"])

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
