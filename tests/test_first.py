import pytest as pytest

from main import app
import json
from flask import Flask, request, jsonify, make_response
import utility as ut
from constants import *
from models import *
from schemas import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_bcrypt import check_password_hash
import jwt
import bcrypt

'''
coverage run -m pytest tests/
coverage report
'''

from sqlalchemy import orm, create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URL = "mysql+mysqlconnector://root:Hondaday13@localhost:3306/pp_base_student_rank"
engine = create_engine(DB_URL)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


app_context = app.app_context()
app_context.push()

client = app.test_client()

'''@pytest.fixture
def app():
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine, )
    app = create_app()
    return app
'''
'''
def test_create_user():
    session = Session()
    try:
        send_data = {
            "username": "stepan",
            "first_name": "Stepan",
            "last_name": "Bandera",
            "password": "batko",
            "email": "batko@mail.ua",
            "phone": "+380000000000",
            "login": "stepan",
            "super_user": False
        }
    
        url = BASE_PATH + USER_PATH
        response = client.post(url, data=json.dumps(send_data), content_type='application/json')
        # session.query(User).filter_by(username = send_data["username"]).delete()
        assert response.status_code == 201
    except:
        session.rollback()
'''
#username
def test_create_user_invalid():
    session = Session()
    try:
        send_data = {
            'username': "solomchaak",
            'first_name': "Ivan",
            'last_name': "Solomchak",
            'password': "0000",
            'email': "pytest@gmail.com",
            'phone': "+380969996969",
            "login": "pytest",
            "super_user": False
        }

        url = BASE_PATH + USER_PATH
        response = client.post(url, data=json.dumps(send_data), content_type='application/json')
        assert response.status_code == 400
    except:
        session.rollback()

#email
def test_create_user_invalid_1():
    session = Session()
    try:
        send_data = {
            "username": "pytest1",
            "first_name": "pytest1",
            "last_name": "pytest1",
            "password": "pytest1",
            "email": "admin@gmail.com",
            "phone": "+380663336633",
            "login": "pytest1",
            "super_user": False
        }

        url = BASE_PATH + USER_PATH
        response = client.post(url, data=json.dumps(send_data), content_type='application/json')
        assert response.status_code == 400
    except:
        session.rollback()

#phone
def test_create_user_invalid_2():
    session = Session()
    try:
        send_data = {
            "username": "pytest2",
            "first_name": "pytest2",
            "last_name": "pytest2",
            "password": "pytest2",
            "email": "pytest2@gmail.com",
            "phone": "+380999977777",
            "login": "pytest2",
            "super_user": False
        }

        url = BASE_PATH + USER_PATH
        response = client.post(url, data=json.dumps(send_data), content_type='application/json')
        assert response.status_code == 400
    except:
        session.rollback()


#login
def test_create_user_invalid_3():
    session = Session()
    try:
        send_data = {
            "username": "pytest3",
            "first_name": "pytest3",
            "last_name": "pytest3",
            "password": "pytest3",
            "email": "pytest3@gmail.com",
            "phone": "+380505554321",
            "login": "urasuk",
            "super_user": False
        }

        url = BASE_PATH + USER_PATH
        response = client.post(url, data=json.dumps(send_data), content_type='application/json')
        assert response.status_code == 400
    except:
        session.rollback()

'''
def test_get_user():
    session = Session()
    user = session.query(User).filter_by(username="urasuk").first()
    access_token = create_access_token(identity='urasuk')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + USER_PATH + '/' + str(user.username)
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "email": "exampl@gmail.com",
        "first_name": "Yurii",
        "last_name": "Yanio",
        "login": "urasuk",
        "password": "$2b$12$LRh.CNZpKOR3tsNAj2RAfu9h/7zJqIBTrctFxDaSci7K7erbTvnke",
        "phone": "+380957777666",
        "super_user": 'false',
        "username": "urasuk"
    }'''

def test_get_user_invalid():
    session = Session()
    try:
        user = session.query(User).filter_by(username="urasukk").first()
        access_token = create_access_token(identity='urasuk')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = BASE_PATH + USER_PATH + '/' + str(user.username)
        response = client.get(url, headers=headers)
        assert response.status_code == 404
    except:
        session.rollback()

def test_get_user_invalid1():
    access_token = create_access_token(identity='solomchaak')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + USER_PATH + '/urasuk'
    response = client.get(url, headers=headers)
    assert response.status_code == 403

def test_get_users():
    access_token = create_access_token(identity='adm')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + USER_PATH
    response = client.get(url, headers=headers)
    assert response.status_code == 200

'''
def test_update_user():
    session = Session()
    try:
        send_data = {
            "email": "exampl@gmail.com",
            "first_name": "Yurii",
            "last_name": "Yanio",
            "login": "urasuk",
            "password": "$2b$12$LRh.CNZpKOR3tsNAj2RAfu9h/7zJqIBTrctFxDaSci7K7erbTvnke",
            "phone": "+380957777666",
            "super_user": 'false',
            "username": "urasuk"
        }
        user = session.query(User).filter_by(username="urasuk").first()
        access_token = create_access_token(identity=user.username)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = BASE_PATH + USER_PATH + '/' + str(user.username)
        response = client.put(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
        send_data = {
            "username": "pipas",
            "firstName": "abdul",
            "lastName": "hamid",
            "password": "Basilokss",
            "email": "ia@mail.ua",
            "phone": "+38066066053"
        }

        user = session.query(User).filter_by(username="pipasd").first()
        access_token = create_access_token(identity=user.username)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = '/api/v1/user/' + str(user.id)
        response = client.put(url, data=json.dumps(send_data), content_type='application/json', headers=headers)

        assert response.status_code == 200
        send_data = {
            "username": "pipas",
            "password": "Basilokss"
        }
        url = '/api/v1/login'
        response = client.get(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
        assert response.status_code == 200
        user = session.query(User).filter_by(username="pipas").delete()
        session.commit()
    except:
        session.rollback()
'''
'''
def test_delete_user():
    session = Session()
    send_data = {
        "username": "nick",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }
    url = BASE_PATH + USER_PATH
    response = client.post(url, data=json.dumps(send_data), content_type='application/json')
    session.commit()

    #видаяємо щойно створений файл
    user = session.query(User).filter_by(username="urasuk").first()
    access_token = create_access_token(identity='adm')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + USER_PATH + '/urasuk'
    response = client.delete(url, headers=headers)
    session.commit()
    assert response.status_code == 200
'''
'''
def test_create_student():
    session = Session()
    send_data = {
        "id": 6,
        "student_age": 19,
        "student_average_grade": 4,
        "student_first_name": "Maksym",
        "student_last_name": "Tkach"
    }

    access_token = create_access_token(identity='adm')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + STUDENT_PATH
    response = client.post(url, headers=headers, data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 201
'''
def test_create_student_invalid():
    try:
        session = Session()
        send_data = {
            "id": 3,
            "student_age": 19,
            "student_average_grade": 4,
            "student_first_name": "Maksym",
            "student_last_name": "Tkach"
        }

        access_token = create_access_token(identity='adm')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = BASE_PATH + STUDENT_PATH
        response = client.post(url, headers=headers, data=json.dumps(send_data), content_type='application/json')
        assert response.status_code == 400
    except:
        session.rollback()

def test_create_student_invalid1():
    try:
        session = Session()
        send_data = {
            "id": 9,
            "student_age": 19,
            "student_average_grade": 4,
            "student_first_name": "Maksym",
            "student_last_name": "Tkach"
        }

        access_token = create_access_token(identity='urasuk')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = BASE_PATH + STUDENT_PATH
        response = client.post(url, headers=headers, data=json.dumps(send_data), content_type='application/json')
        assert response.status_code == 403
    except:
        session.rollback()

'''def test_create_student_invalid2():
    send_data = {
        "id": 9,
        "student_age": 19,
        "student_first_name": "Maksym",
        "student_last_name": "Tkach"
    }

    access_token = create_access_token(identity='urasuk')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + STUDENT_PATH
    response = client.post(url, headers=headers, data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 400
'''

def test_get_students():
    url = BASE_PATH + STUDENT_PATH
    response = client.get(url)
    assert response.status_code == 200
'''
def test_get_student():
    url = BASE_PATH + STUDENT_PATH + '/2'
    response = client.get(url)
    assert response.status_code == 200
    assert json.loads(response.data) == {
    "id": 2,
    "student_age": 18,
    "student_average_grade": 4,
    "student_first_name": "Viktoria",
    "student_last_name": "Molochii"
    }
'''
def test_get_student_invalid():
    session = Session()
    student = session.query(Student).filter_by(id=10).first()
    url = BASE_PATH + STUDENT_PATH + '/10'
    response = client.get(url)
    assert response.status_code == 404


'''
def test_create_rank():
    session = Session()
    send_data = {
        "changed_by": "vv",
        "last_change": "2021-11-11T10:37:52",
        "rank_id": 7,
        "student_id": 3
    }

    access_token = create_access_token(identity='adm')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = BASE_PATH + RANK_PATH
    response = client.post(url, headers=headers, data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 201
'''
'''
def test_get_rating():
    url = BASE_PATH + RANK_PATH + RATING_PATH
    response = client.get(url)
    assert response.status_code == 200
'''
'''
def test_create_event():
    send_data = {
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }

    url = '/api/v1/user'
    response = client.post(url, data=json.dumps(send_data), content_type='application/json')
    session.commit()
    user = session.query(User).filter_by(username="pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    send_data = {
        'header': "something",
        'description': "something",
        'date': "2011-11-03 18:21:26"
    }
    url = '/api/v1/events'
    response = client.post(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
    session.commit()
    assert response.status_code == 200
    url = '/api/v1/system'
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    send_data = {
        'header': "somethin",
        'description': "somethin",
        'date': "2011-11-03 18:21:25"
    }
    temp = session.query(Events).order_by(Events.id.desc()).first()
    url = '/api/v1/events/' + str(temp.id)
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    response = client.put(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
    session.commit()
    assert response.status_code == 200
    session.query(System).filter_by(userId=user.id).delete()
    session.query(User).filter_by(id=user.id).delete()
    session.query(Events).filter_by(header="somethin").delete()
    session.commit()


def test_get_events():
    url = '/api/v1/events'
    response = client.get(url)
    assert response.status_code == 200


def test_delete_events():
    send_data = {
        "username": "pipasd",
        "firstName": "abdul",
        "lastName": "hamid",
        "password": "Basiloks",
        "email": "iam@mail.ua",
        "phone": "+380665066053"
    }

    url = '/api/v1/user'
    response = client.post(url, data=json.dumps(send_data), content_type='application/json')
    session.commit()
    user = session.query(User).filter_by(username="pipasd").first()
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    send_data = {
        'header': "some",
        'description': "something",
        'date': "2011-11-03 18:21:26"
    }
    url = '/api/v1/events'
    response = client.post(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
    session.commit()
    temp = session.query(Events).order_by(Events.id.desc()).first()
    session.commit()
    session.query(System).filter_by(userId=user.id).delete()
    session.commit()
    url = '/api/v1/events/' + str(temp.id)
    response = client.delete(url, headers=headers)
    session.query(User).filter_by(id=user.id).delete()
    session.commit()
    assert response.status_code == 200
'''
