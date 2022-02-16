
from flask import Flask, jsonify, make_response, request
from .entities import Career, Convocation, ConvocationApplicant, DocumentType, Person, Play, Student
from .orm.globals import Globals
from .orm.connection import Connection
from .orm.query import FetchMode, Query
import atexit

try:
    Globals.set('connection', Connection())
except Exception as ex:
    print(f"Could not connect to database\nCause: {ex}")


app = Flask(__name__)


@app.get('/play')
def get_plays():
    """
    Returns a list of plays
    """
    plays = Query(Play.GET_ALL_QUERY).execute(fetch=FetchMode.ALL)

    return jsonify(plays)


@app.get('/play/<int:play_id>/convocation/applicants')
def get_play_applicants(play_id: int):
    """
    Returns a lis of students that have applied to a certain play
    """

    students = Query(Student.GET_STUDENTS_APPLIED_TO_PLAY,
                     play_id=play_id).execute(fetch=FetchMode.ALL)

    return jsonify(students)


@app.post('/play/<int:play_id>/convocation')
def create_convocation_for_play(play_id: int):
    json_data = request.json

    if not json_data['code']:
        return make_response(jsonify({
            'message': 'No student code provided'
        }), 400)

    student = Query(Student.CHECK_BY_CODE, code=json_data['code']).execute(
        fetch=FetchMode.ONE)

    if not student:
        return make_response(jsonify({
            'message': 'There\'s not an student with that code'
        }), 404)

    convocation = Query(Convocation.CHECK_BY_PLAY,
                        play_id=play_id).execute(fetch=FetchMode.ONE)

    if not convocation:
        return make_response(jsonify({
            'message': 'The current play does not have any convocations'
        }), 400)

    # create convocation applicant
    Query(ConvocationApplicant.SAVE_NEW,
          convocation_id=convocation['id'],
          student_code=student['code'],
          doc_number=student['doc_number']
          ).execute()

    return make_response(jsonify({
        'message': 'Convocation successfuly applied'
    }), 201)


@app.get('/student/<string:code>')
def get_student(code: str):
    """
    Returns a student if found by code. Otherwise will return an empty
    object with a 404 status code

    :param code: code of the student
    """
    student = Query(Student.GET_BY_CODE, code=code).execute(
        fetch=FetchMode.ONE)

    if not student:
        return make_response(jsonify({}), 404)

    return jsonify(student)


@app.get('/student/<string:code>/convocations')
def get_student_convocation_plays(code: str):
    """
    Returns a list of plays a given student has applied in a convocation for

    :param code: Code of the student
    """

    plays = Query(Play.GET_PLAYS_BY_STUDENT_CONVOCATION,
                  code=code).execute(fetch=FetchMode.ALL)

    return jsonify(plays)


@app.get('/document-type')
def get_document_types():
    document_types = Query(DocumentType.GET_ALL).execute(fetch=FetchMode.ALL)

    return jsonify(document_types)


@app.get('/career')
def get_careers():
    careers = Query(Career.GET_ALL).execute(fetch=FetchMode.ALL)

    return jsonify(careers)


@app.post('/student')
def create_student():
    """
    Creates an student
    """
    json_data = request.json

    if not json_data['docNumber'] or not json_data['documentTypeId'] or not json_data['names'] \
            or not json_data['lastName'] or not json_data['birthDate'] or not json_data['email'] \
    or not json_data['code'] or not json_data['careerId']:
        return make_response(jsonify({
            'message': 'Missing fields'
        }), 400)

    if Query(Person.GET_BY_DOC, code=json_data['docNumber']).execute(fetch=FetchMode.ONE):
        return make_response(jsonify({
            'message': 'There\'s already a person with that document number',
        }), 422)

    if Query(Student.CHECK_BY_CODE, code=json_data['code']).execute(fetch=FetchMode.ONE):
        return make_response(jsonify({
            'message': 'There\'s already a student with that code'
        }), 422)

    # create person
    Query(Person.SAVE_NEW,
          doc_number=json_data['docNumber'],
          document_type_id=json_data['document_type_id'],
          names=json_data['names'],
          last_name=json_data['last_name'],
          birth_date=json_data['birthDate'],
          email=json_data['email']
          ).execute()

    Query(Student.SAVE_NEW,
          doc_number=json_data['docNumber'],
          code=json_data['code'],
          career_id=json_data['careerId']
          ).execute()

    return make_response(jsonify({
        'message': 'student created'
    }), 201)


def exit_handler():
    Globals.get('connection').close()


atexit.register(exit_handler)
