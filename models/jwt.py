from manager.db import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from contextlib import contextmanager


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        session.close()


class JWTToken(db.Model):
    __tablename__ = "TB_PY_JWT"

    id = Column(Integer, primary_key=True)
    token = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey("TB_PY_USER.id"), nullable=False)
    createdtime = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship("User", backref="tokens")

    def __repr__(self):
        return f"<JWTToken {self.token} for User ID {self.user_id}>"

    @classmethod
    def create(cls, token, user_id):
        with session_scope() as session:
            new_token = cls(token=token, user_id=user_id)
            session.add(new_token)
            return new_token

    def is_expired(self, expiration_hours=1):
        """Check if the token is expired based on the creation time."""
        return datetime.now() > self.createdtime + timedelta(hours=expiration_hours)
