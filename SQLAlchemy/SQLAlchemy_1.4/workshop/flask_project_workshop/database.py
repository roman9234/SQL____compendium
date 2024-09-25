from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import declarative_base, relationship

db = SQLAlchemy()


class Employee(db.Model):
    # __tablename__ = "user_account"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=func.now())

    department_id = db.Column(db.Integer, db.ForeignKey("department.id", ondelete="SET NULL"))
    # back_populates ссылается на противоположное поле
    department = relationship("Department", back_populates="employees")
    def __repr__(self):
        return f"User(fullname={self.fullname!r}"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    employees = relationship("Employee", back_populates="department")

    def __repr__(self):
        return f"Department(name={self.name!r}"
