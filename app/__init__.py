from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "my_super_secret_key_123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    from app.routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app