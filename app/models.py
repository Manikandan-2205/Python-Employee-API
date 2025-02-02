from datetime import datetime
from app.db import get_db_session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "TB_PY_USER"

    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    createdby = Column(Integer, nullable=False)
    createdtime = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedby = Column(Integer, nullable=True)
    updatedtime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )
    isdeleted = Column(String(1), nullable=False, default="N")
    isdisable = Column(String(1), nullable=False, default="N")

    def __repr__(self):
        return f"<User  {self.username}>"

    @classmethod
    def create(cls, username, password, role, createdby):
        """Creates a new User in the database."""
        with get_db_session() as session:
            try:
                new_user = cls(
                    username=username,
                    password=password,
                    role=role,
                    createdby=createdby,
                    updatedby=createdby,
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                return new_user
            except IntegrityError:
                session.rollback()
                return {"error": "Username already exists."}
            except Exception as ex:
                session.rollback()
                return {"error": str(ex)}

    @classmethod
    def get_all(cls):
        """Fetch all users."""
        with get_db_session() as session:
            return session.query(cls).filter_by(isdeleted="N").all()

    @classmethod
    def get_by_id(cls, user_id):
        """Fetch a user by ID."""
        with get_db_session() as session:
            return session.query(cls).filter_by(id=user_id, isdeleted="N").first()

    @classmethod
    def get_by_any(cls, **kwargs):
        """Fetch users by any field matching the provided keyword arguments."""
        with get_db_session() as session:
            query = session.query(cls).filter_by(isdeleted="N")
            for key, value in kwargs.items():
                if hasattr(cls, key):
                    query = query.filter(getattr(cls, key).like(f"%{value}%"))
            return query.all()

    @classmethod
    def update(cls, user_id, **kwargs):
        """Update a user record."""
        with get_db_session() as session:
            user = session.query(cls).filter_by(id=user_id, isdeleted="N").first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.updatedtime = datetime.now()  # Update the timestamp
                session.commit()
                return user
            return {"error": "User  not found."}


class JWTToken(Base):
    __tablename__ = "TB_PY_JWT"

    id = Column(Integer, primary_key=True)
    token = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("TB_PY_USER.id"), nullable=False)
    createdtime = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User ", backref="tokens")

    def __repr__(self):
        return f"<JWTToken {self.token} for User ID {self.user_id}>"

    @classmethod
    def get_all(cls):
        """Fetch all JWT tokens, ordered by createdtime descending."""
        with get_db_session() as session:
            return session.query(cls).order_by(cls.createdtime.desc()).all()

    @classmethod
    def get_by_id(cls, token_id):
        """Fetch a JWT token by ID."""
        with get_db_session() as session:
            return session.query(cls).filter_by(id=token_id).first()


class UserLog(Base):
    __tablename__ = "TB_PY_USER_LOG"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("TB_PY_USER.id"), nullable=False)
    logintime = Column(DateTime, default=datetime.utcnow, nullable=False)
    logouttime = Column(DateTime, nullable=True)
    jwt_id = Column(Integer, ForeignKey("TB_PY_JWT.id"), nullable=True)
    status = Column(String(1), default="N", nullable=False)

    # Relationships
    user = relationship("User ", backref="logs")
    jwt_token = relationship("JWTToken", backref="user_logs")

    def __repr__(self):
        return f"<User Log user_id={self.user_id}, logintime={self.logintime}, status={self.status}>"

    @classmethod
    def create_log(cls, user_id, jwt_id, status="N"):
        """Creates a new user login log entry."""
        with get_db_session() as session:
            new_log = cls(user_id=user_id, jwt_id=jwt_id, status=status)
            session.add(new_log)
            session.commit()
            session.refresh(new_log)
            return new_log

    @classmethod
    def get_logs_by_user(cls, user_id):
        """Fetch all logs for a specific user."""
        with get_db_session() as session:
            return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def get_all_logs(cls):
        """Fetch all user logs."""
        with get_db_session() as session:
            return session.query(cls).all()


class Employee(Base):
    __tablename__ = "TB_PY_EMPLOYEE"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"

    @classmethod
    def create(cls, first_name, last_name, email):
        """Creates a new employee in the database."""
        with get_db_session() as session:
            try:
                new_employee = cls(
                    first_name=first_name, last_name=last_name, email=email
                )
                session.add(new_employee)
                session.commit()
                session.refresh(new_employee)
                return new_employee
            except IntegrityError:
                session.rollback()
                return None
            except Exception as ex:
                return ex

    @classmethod
    def get_all(cls):
        """Fetch all employees."""
        with get_db_session() as session:
            return session.query(cls).all()

    @classmethod
    def get_by_id(cls, emp_id):
        """Fetch an employee by ID."""
        with get_db_session() as session:
            return session.query(cls).filter_by(id=emp_id).first()
