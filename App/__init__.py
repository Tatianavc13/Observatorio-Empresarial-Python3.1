import os
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User  # importa el modelo usuario

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar Blueprints
    from .auth.routes import auth_bp
    from .flashes.routes import flashes_bp, public_bp, api_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(flashes_bp, url_prefix="/admin")
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
