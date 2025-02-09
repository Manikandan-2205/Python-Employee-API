# manager/config.py
import os
import secrets


class Config:
    db_directory = "db"

    # Create the database directory if it doesn't exist
    os.makedirs(db_directory, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.abspath(os.path.join(db_directory, 'FlaskAPI.db'))}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")

    def generate_jwt_secret_key():
        return secrets.token_hex(32)

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", generate_jwt_secret_key())
