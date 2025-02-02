from flask import Flask
from flask_migrate import Migrate
from app.views import api_bp
from app.config import Config
from app.db import get_db_engine
from app.cache import cache

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize cache
    cache.init_app(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    return app


def init_migrate(app):
    migrate.init_app(app, get_db_engine())
