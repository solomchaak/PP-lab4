from flask import Flask, request, jsonify
import utility
from constants import *
from models import *
from schemas import *
import bcrypt

app = Flask(__name__)

@app.route("/api/v1/hello-world-12")
def hello_world():
    return "<p>Hello, World! 12</p>"

#---------------USER----------------
@app.route(BASE_PATH + USER_PATH + '/<Username>', methods=['GET'])
def get_user_by_username(Username):
    session = Session()
    try:
        user = session.query(User).filter_by(username=Username).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    return jsonify(UserSchema().dump(user)), 200

@app.route(BASE_PATH + USER_PATH, methods=['GET'])
def get_all_users():
    session = Session()
    try:
        users = session.query(User).all()
    except:
        users = []

    users_dto = UserSchema(many=True)

    return jsonify(users_dto.dump(users)), 200

@app.route(BASE_PATH + USER_PATH, methods=['POST'])
def create_user():
    session = Session()
    try:
        user_data = UserSchema().load(request.json)
        try:
            if (session.query(User).filter_by(username = user_data.get('username').one())):
                return jsonify(USER_ALREADY_EXISTS), 409
        except: pass
        # password hashing ------------------------------------
        passwd = user_data.get('password')
        hashed_password = bcrypt.hashpw(bytes(passwd, 'utf-8'), bcrypt.gensalt())
        user_data['password'] = hashed_password
        # -----------------------------------------------------
        new_user = User(**user_data)
        session.add(new_user)
        session.commit()
        return jsonify(USER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

@app.route(BASE_PATH + USER_PATH + '/<Username>', methods=['PUT'])
def update_user(Username):
    session = Session()
    try:
        try:
            user = session.query(User).filter_by(username=Username).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        user_data = UserSchema().load(request.json, partial=True)
        if user_data.get('username'):
            return jsonify(CANT_CHANGE_IDENTIFIER), 400
    except:
        pass
    try:
        if user_data.get('password'):
            # password hashing ------------------------------------
            passwd = user_data.get('password')
            hashed_password = bcrypt.hashpw(bytes(passwd, 'utf-8'), bcrypt.gensalt())
            user_data['password'] = hashed_password
            # -----------------------------------------------------
        updated_user = utility.update_entry(user, **user_data)

        if updated_user == None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        return jsonify(USER_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

@app.route(BASE_PATH + USER_PATH + '/<Username>', methods=['DELETE'])
def delete_user(Username):
    session = Session()
    try:
        user = session.query(User).filter_by(username=Username).one()
    except:
        return jsonify(USER_NOT_FOUND), 404
    session.delete(user)
    session.commit()

    return jsonify(USER_DELETED), 200

#-------------STUDENT---------------
@app.route(BASE_PATH + STUDENT_PATH, methods=['POST'])
def create_student():
    session = Session()
    try:
        student_data = StudentSchema().load(request.json)
        try:
            if (session.query(Student).filter_by(id=student_data.get('id').one())):
                return jsonify(STUDENT_ALREADY_EXISTS), 409
        except:
            pass

        new_student = Student(**student_data)
        session.add(new_student)
        session.commit()
        return jsonify(STUDENT_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

@app.route(BASE_PATH + STUDENT_PATH, methods=['GET'])
def get_all_students():
    session = Session()
    try:
        students = session.query(Student).all()
    except:
        students = []

    students_dto = StudentSchema(many=True)

    return jsonify(students_dto.dump(students)), 200

@app.route(BASE_PATH + STUDENT_PATH + '/<Id>', methods=['GET'])
def get_student_by_id(Id):
    session = Session()
    try:
        student = session.query(Student).filter_by(id=Id).one()
    except:
        return jsonify(STUDENT_NOT_FOUND), 404

    return jsonify(StudentSchema().dump(student)), 200

@app.route(BASE_PATH + STUDENT_PATH + '/<Id>', methods=['PUT'])
def update_student(Id):
    session = Session()
    try:
        try:
            student = session.query(Student).filter_by(id=Id).one()
        except:
            return jsonify(STUDENT_NOT_FOUND), 404

        student_data = StudentSchema().load(request.json, partial=True)
        if student_data.get('id'):
            return jsonify(CANT_CHANGE_IDENTIFIER), 400
    except:
        pass
    try:
        updated_student = utility.update_entry(student, **student_data)

        if updated_student == None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        return jsonify(STUDENT_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

@app.route(BASE_PATH + STUDENT_PATH + '/<Id>', methods=['DELETE'])
def delete_student(Id):
    session = Session()
    try:
        student = session.query(Student).filter_by(id=Id).one()
    except:
        return jsonify(STUDENT_NOT_FOUND), 404
    session.delete(student)
    session.commit()

    return jsonify(STUDENT_DELETED), 200

#---------------RANK----------------
@app.route(BASE_PATH + RANK_PATH, methods=['POST'])
def create_rank():
    session = Session()
    try:
        rank_data = RankSchema().load(request.json)
        try:
            if (session.query(Rank).filter_by(rank_id=rank_data.get('rank_id').one())):
                return jsonify(RANK_ALREADY_EXISTS), 409
        except:
            pass

        new_rank = Rank(**rank_data)
        session.add(new_rank)
        session.commit()
        return jsonify(RANK_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

@app.route(BASE_PATH + RANK_PATH + '/<Id>', methods=['GET'])
def get_rank_by_id(Id):
    session = Session()
    try:
        rank = session.query(Rank).filter_by(rank_id=Id).one()
    except:
        return jsonify(RANK_NOT_FOUND), 404

    return jsonify(RankSchema().dump(rank)), 200

@app.route(BASE_PATH + RANK_PATH, methods=['GET'])
def get_all_ranks():
    session = Session()
    try:
        ranks = session.query(Rank).all()
    except:
        ranks = []

    ranks_dto = RankSchema(many=True)

    return jsonify(ranks_dto.dump(ranks)), 200

@app.route(BASE_PATH + RANK_PATH + RATING_PATH, methods=['GET'])
def get_rating():
    session = Session()
    try:
        rating = session.query(Student).join(Rank).filter(Rank.student_id == Student.id).order_by(desc(Student.student_average_grade))
    except:
        rating = []

    rating_dto = StudentSchema(many=True)

    return jsonify(rating_dto.dump(rating)), 200

@app.route(BASE_PATH + RANK_PATH + '/<Id>', methods=['PUT'])
def update_rank(Id):
    session = Session()
    try:
        try:
            rank = session.query(Rank).filter_by(rank_id=Id).one()
        except:
            return jsonify(RANK_NOT_FOUND), 404

        rank_data = RankSchema().load(request.json, partial=True)
        if rank_data.get('rank_id'):
            return jsonify(CANT_CHANGE_IDENTIFIER), 400
    except:
        pass
    try:
        updated_rank = utility.update_entry(rank, **rank_data)

        if updated_rank == None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        return jsonify(RANK_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

@app.route(BASE_PATH + RANK_PATH + '/<Id>', methods=['DELETE'])
def delete_rank(Id):
    session = Session()
    try:
        rank = session.query(Rank).filter_by(rank_id=Id).one()
    except:
        return jsonify(RANK_NOT_FOUND), 404

    session.delete(rank)
    session.commit()

    return jsonify(RANK_DELETED), 200