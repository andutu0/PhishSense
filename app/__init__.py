from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    with app.app_context():
        from . import routes
    
    return app