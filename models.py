import os
import sys

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy import orm, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship



DB_URL = "mysql+mysqlconnector://root:Hondaday13@localhost:3306/pp_base_student_rank"

engine = create_engine(DB_URL)

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    username = Column(String(length=45), primary_key=True, unique=True)
    first_name = Column(String(length=45), nullable=False)
    last_name = Column(String(length=45), nullable=False)
    email = Column(String(length=45), nullable=False, unique=True)
    phone = Column(String(length=45), nullable=True, unique=True)
    login = Column(String(length=45), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)
    super_user = Column(Boolean, nullable=False)

    child_rank = relationship("Rank")

    def __str__(self):
        return f"username : {self.username}\n" \
               f"first name : {self.first_name}\n" \
               f"last name : {self.last_name}\n" \
               f"email : {self.email}\n" \
               f"phone : {self.phone}\n" \
               f"login : {self.login}\n" \
               f"super user : {self.super_user}\n" \
               f"password : {self.password}\n"


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True, unique=True)
    student_first_name = Column(String(length=45), nullable=False)
    student_last_name = Column(String(length=45), nullable=False)
    student_average_grade = Column(Integer, nullable=False)
    student_age = Column(Integer, nullable=True)

    child_rank = relationship("Rank")

    def __str__(self):
        return f"ID : {self.id}\n" \
               f"first name : {self.student_first_name}\n" \
               f"last name : {self.student_last_name}\n" \
               f"average grade : {self.student_average_grade}\n" \
               f"age : {self.student_age}\n"

class Rank(Base):
    __tablename__ = "Rank"

    rank_id = Column(Integer, primary_key=True, unique=True)
    student_id = Column(Integer, ForeignKey("Student.id"), nullable=False)
    last_change = Column(TIMESTAMP, nullable=False)
    changed_by = Column(String(length=45), ForeignKey("User.username"), nullable=False)

    def __str__(self):
        return f"rank id : {self.id}\n" \
               f"student id : {self.student_first_name}\n" \
               f"last change : {self.student_last_name}\n" \
               f"changed by : {self.student_average_grade}\n"

    # child_user = orm.relationship("User")
    # child_student = orm.relationship("Student")

# alembic revision --autogenerate -m "second"
# alembic upgrade head
