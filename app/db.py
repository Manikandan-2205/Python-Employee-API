from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine():
    database_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]
    return create_engine(
        database_uri, connect_args={"check_same_thread": False}
    )  # SQLite requires this for multi-threading


def get_db_session():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()
