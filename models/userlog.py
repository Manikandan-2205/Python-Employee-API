from contextlib import contextmanager
from manager.db import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


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


class UserLog(db.Model):
    __tablename__ = "TB_PY_USER_LOG"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("TB_PY_USER.id"), nullable=False)
    logintime = Column(DateTime, default=datetime.now, nullable=False)
    logouttime = Column(DateTime, nullable=True)
    status = Column(String(1), default="N", nullable=False)

    user = relationship("User", backref="logs")

    def __repr__(self):
        return f"<User  Log user_id={self.user_id}, logintime={self.logintime}>"

    @classmethod
    def create_log(cls, user_id):
        """Create a new user log entry."""
        new_log = cls(user_id=user_id, logintime=datetime.now(), status="Y")
        with session_scope() as session:
            session.add(new_log)
            return new_log

    @classmethod
    def get_logs_by_user(cls, user_id):
        """Retrieve all logs for a specific user."""
        with session_scope() as session:
            return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def get_all_logs(cls):
        """Retrieve all user logs."""
        with session_scope() as session:
            return session.query(cls).all()
