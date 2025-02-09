# models/employee.py
from manager.db import db  
from sqlalchemy import Column, Integer, String

class Employee(db.Model):
    __tablename__ = "TB_PY_EMPLOYEE"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"

    @classmethod
    def create(cls, first_name, last_name, email):
        new_employee = cls(first_name=first_name, last_name=last_name, email=email)
        db.session.add(new_employee)
        db.session.commit()
        return new_employee

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, emp_id):
        return cls.query.get(emp_id)