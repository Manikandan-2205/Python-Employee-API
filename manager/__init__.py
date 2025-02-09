import os
from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
from manager.config import Config
from manager.db import db
from sqlalchemy import text
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object(Config)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Setup Swagger with Bearer Authentication
    swagger = Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Employee.API",
                "version": "1.0",
                "description": "API documentation for your application.",
            },
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Enter 'Bearer <JWT>' in the text input below.",
                }
            },
            "security": [
                {"Bearer": []}
            ],  
            "paths": {},
        },
    )

    db.init_app(app)

    with app.app_context():
        with db.engine.connect() as connection:
            connection.execute(text("PRAGMA journal_mode=WAL;"))

    migrate = Migrate(app, db)

    db_directory = Config.db_directory
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)


    from models.employee import Employee
    from models.user import User
    from models.jwt import JWTToken
    from models.userlog import UserLog

    from blueprints.employee import emp_bp
    from blueprints.user import user_bp
    from blueprints.jwt import jwt_bp
    from blueprints.userlog import log_bp

    # Register blueprints with the appropriate URL prefixes
    app.register_blueprint(emp_bp, url_prefix="/api/employees")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(jwt_bp, url_prefix="/api/jwt")
    app.register_blueprint(log_bp, url_prefix="/api/logs")

    return app


app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "True") == "True"
    port = int(os.getenv("FLASK_PORT", 5002))
    app.run(debug=debug_mode, port=port)
