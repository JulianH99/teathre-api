
import atexit
from functools import wraps

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from itsdangerous import json
from jinja2 import Template

from .mail import send_mail

from .entities import (Career, Character, Convocation, ConvocationApplicant, ConvocationDates,
                       DocumentType, Person, Play, Student, StudentAssistance)
from .orm.connection import Connection
from .orm.globals import Globals
from .orm.query import FetchMode, Query

try:
    print("Connecting to db")
    Globals.set('connection', Connection())
except Exception as ex:
    print(f"Could not connect to database\nCause: {ex}")


print("App ready")
app = Flask(__name__)
cors = CORS(app)

USER_ID_HEADER_NAME = 'X-User-Id'


def has_teacher_id_header(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):
        headers = request.headers
        if headers.get(USER_ID_HEADER_NAME) is None:
            return make_response(jsonify({'message': 'User id was not provided'}), 403)
        return function(*args, **kwargs)

    return decorated_function


@app.get('/tab/assistance')
@has_teacher_id_header
def get_enabled_asistance_tab():
    teacher_id = request.headers.get(USER_ID_HEADER_NAME)

    active_play = Query(Play.GET_ACTIVE_PLAY_BY_TEACHER,
                        employee_id=teacher_id).execute(fetch=FetchMode.ONE)

    if not active_play:
        return jsonify({"active": False})

    return jsonify({"active": True, "play": active_play})


@app.get('/play/<int:play_id>/students')
@has_teacher_id_header
def get_play_students(play_id: int):
    students = Query(Student.GET_STUDENTS_BY_PLAY,
                     play_id=play_id).execute(fetch=FetchMode.ALL)

    return jsonify(students)


@app.post('/play/<int:play_id>/event/<int:play_event_id>/assistance')
@has_teacher_id_header
def save_students_assistance_to_play(play_id: int, play_event_id: int):
    students_list = request.json

    for student in students_list:
        Query(StudentAssistance.SAVE_NEW_ASSISTANCE, play_id=play_id,
              play_event_id=play_event_id, student_code=student)

    return jsonify({"message": "Students assistance saved"})


def exit_handler():
    Globals.get('connection').close()


atexit.register(exit_handler)
