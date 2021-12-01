import os
import sys

from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    DateTime,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy import orm, create_engine
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
    password = Column(String(length=100), nullable=False)

    child_rank = relationship("Rank")

    def __str__(self):
        return f"username : {self.UserName}\n" \
               f"first name : {self.firstName}\n" \
               f"last name : {self.lastName}\n" \
               f"email : {self.email}\n" \
               f"phone : {self.phone}\n" \
               f"password : {self.password}\n"


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True, unique=True)
    student_first_name = Column(String(length=45), nullable=False)
    student_last_name = Column(String(length=45), nullable=False)
    student_average_grade = Column(DECIMAL(10, 2), nullable=False)
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

    #child_student = relationship("student")
    #child_user = relationship("user")

    def __str__(self):
        return f"rank id : {self.id}\n" \
               f"student id : {self.student_first_name}\n" \
               f"last change : {self.student_last_name}\n" \
               f"changed by : {self.student_average_grade}\n"

    # child_user = orm.relationship("User")
    # child_student = orm.relationship("Student")

# alembic revision --autogenerate -m "First"
# alembic upgrade head

'''
from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

DB_URL = "mysql+mysqlconnector://root:Hondaday13@localhost:3306/pp_base_student_rank"

engine = create_engine(DB_URL)

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key = True)
    name = Column(String(45), nullable = False)
    surname = Column(String(45), nullable = False)
    username = Column(String(45), nullable = False)
    password = Column(String(1000))
    accessusers = Column(String(45))
    children3 = relationship("Rating")
    def repr(self):
        return f"{self.id}, {self.name}, {self.surname}, {self.username}, {self.password},{self.accessusers} "


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key = True)
    firstname = Column(String(45), nullable = False)
    surname = Column(String(45), nullable = True)
    course = Column(Integer, nullable = True)
    best_grade = Column(Integer)
    children = relationship("Rating")

    def repr(self):
        return f"{self.id}, {self.firstname}, {self.surname}, {self.course}, {self.best_grade} "

class Rating(Base):
    __tablename__ = "Rating"

    id = Column(Integer, primary_key = True)
    title = Column(String(45), nullable = False)
    Student_id = Column(Integer, ForeignKey('Student.id'))
    user_creator_id = Column(Integer, ForeignKey('User.id'))

    def repr(self):
        return f"{self.id}, {self.title}, {self.Student_id}, {self.accessus} "

class Properties(Base):
    __tablename__ = "Propeties"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    rating_id = Column(Integer, ForeignKey('Rating.id'))
    children1 = relationship("Rating")
    children2 = relationship("User")

    def repr(self):
        return f"{self.id}, {self.user_id}, {self.rating_id} "
'''