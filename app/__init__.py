from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    with app.app_context():
        from . import routes
    
    return app