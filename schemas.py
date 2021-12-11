from models import User, Student, Rank
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'login', 'super_user', 'password')

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        fields = ('id', 'student_first_name', 'student_last_name', 'student_average_grade', 'student_age')

class RankSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rank
        fields = ('rank_id', 'student_id', 'last_change', 'changed_by')