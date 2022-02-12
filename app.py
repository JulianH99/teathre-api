
from flask import Flask, jsonify, make_response, request
from api.entities import Play, Student
from api.orm.globals import Globals
from api.orm.connection import Connection
from api.orm.query import FetchMode, Query
import atexit

try:
    Globals.set('connection', Connection())
except Exception as ex:
    print(f"Could not connect to database\nCause: {ex}")


app = Flask(__name__)


@app.get('/play')
def get_plays():
    plays = Query(Play.GET_ALL_QUERY).execute(fetch=FetchMode.ALL)

    return jsonify(plays)


@app.get('/student/<string:code>')
def get_student(code: str):

    student = Query(Student.GET_BY_CODE, code=code).execute(
        fetch=FetchMode.ONE)

    if not student:
        return make_response(jsonify({}), 404)

    return jsonify(student)


@app.get('/student/<string:code>/convocations')
def get_student_convocation_plays(code: str):

    plays = Query(Play.GET_PLAYS_BY_STUDENT_CONVOCATION,
                  code=code).execute(fetch=FetchMode.ALL)

    return jsonify(plays)


def exit_handler():
    Globals.get('connection').close()


atexit.register(exit_handler)
