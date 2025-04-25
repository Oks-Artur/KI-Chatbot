# Initialisierung des Flask-Blueprints
from flask import Flask
from .routes import app as app_blueprint

def create_app():
    # Flask-Anwendung erzeugen
    app = Flask(__name__)
    app.register_blueprint(app_blueprint)  # Blueprint registrieren
    return app
