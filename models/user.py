# models/user.py
from manager.db import db  
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import bcrypt 

class User(db.Model):
    __tablename__ = "TB_PY_USER"

    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    createdtime = Column(DateTime, default=datetime.now, nullable=False)
    updatedtime = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    def __repr__(self):
        return f"<User   {self.username}>"

    @classmethod
    def create(cls, username, password, role):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = cls(username=username, password=hashed_password.decode('utf-8'), role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)