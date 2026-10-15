# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# import os


# db = SQLAlchemy()

# login_manager = LoginManager()


# def create_app():

#     app = Flask(__name__)


#     app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#     if not app.config["SECRET_KEY"]:
#         raise RuntimeError("SECRET_KEY is not configured.")


#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"


#     app.config["UPLOAD_FOLDER"] = os.path.join(
#         app.root_path,
#         "static",
#         "uploads"
#     )


#     db.init_app(app)


#     login_manager.init_app(app)

#     login_manager.login_view = "login"


#     # Register existing marketplace routes
#     from app.routes import register_routes

#     register_routes(app)


#     # Register AI Marketplace Copilot routes
#     from app.copilot.routes import register_copilot_routes

#     register_copilot_routes(app)


#     with app.app_context():

#         db.create_all()


#     return app





import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Load .env from the project root, regardless of the terminal's directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=False)

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    secret_key = os.getenv("SECRET_KEY")

    if not secret_key:
        raise RuntimeError(
            f"SECRET_KEY is not configured. Check: {PROJECT_ROOT / '.env'}"
        )

    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path, "static", "uploads"
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from app.routes import register_routes
    from app.copilot.routes import register_copilot_routes

    register_routes(app)
    register_copilot_routes(app)

    with app.app_context():
        db.create_all()

    return app
