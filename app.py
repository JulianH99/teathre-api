
import atexit
from datetime import datetime
import locale
from functools import wraps

from flask import Flask, jsonify, make_response, request, render_template, session, send_file
from flask_cors import CORS

from mail import send_mail

from entities import (Career, Character, Convocation, ConvocationApplicant, ConvocationDates,
                      DocumentType, Person, Play, Student, StudentAssistance, Employee)
from orm.connection import Connection
from orm.globals import Globals
from orm.query import FetchMode, Query
from pdf import html_to_pdf


locale.setlocale(locale.LC_ALL, 'es_CO')

try:
    print("Connecting to db")
    Globals.set('connection', Connection())
except Exception as ex:
    print(f"Could not connect to database\nCause: {ex}")


print("App ready")
app = Flask(__name__)

app.secret_key = 'QKW%Hb253qcpF_'
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


@app.get('/tab/assistance/<int:play_id>')
def get_enabled_asistance_tab(play_id: int):
    teacher_id = request.headers.get(USER_ID_HEADER_NAME)

    active_play = Query(Play.GET_ACTIVE_PLAY_BY_TEACHER,
                        employee_id=teacher_id, play_id=play_id).execute(fetch=FetchMode.ONE)

    if not active_play:
        return jsonify({"active": False})

    return jsonify({"active": True, "play": active_play})


@app.get('/play/<int:play_id>/event/<int:play_event_id>/students')
@has_teacher_id_header
def get_play_students_assistance(play_id: int, play_event_id: int):
    students = Query(Student.GET_STUDENTS_BY_PLAY_ASSISTANCE,
                     play_event_id=play_event_id,
                     play_id=play_id).execute(fetch=FetchMode.ALL)

    return jsonify(students)


@app.post('/play/<int:play_id>/event/<int:play_event_id>/assistance')
@has_teacher_id_header
def save_students_assistance_to_play(play_id: int, play_event_id: int):
    students_list = request.json

    for student in students_list:
        asistance = Query(StudentAssistance.GET_ASSISTANCE, student_code=student,
                          play_event_id=play_event_id, play_id=play_id).execute(FetchMode.ONE)

        if not asistance:
            Query(StudentAssistance.SAVE_NEW_ASSISTANCE, play_id=play_id,
                  play_event_id=play_event_id, student_code=student).execute()

    return jsonify({"message": "Students assistance saved"})


@app.get('/play')
def get_plays():
    state = int(request.args.get('state'))
    if state != 0 and state != 1:
        state = 1

    plays = Query(Play.GET_ALL_QUERY_STATE, state=state).execute(FetchMode.ALL)

    return jsonify(plays)


@app.get('/plays')
def get_plays_all():

    plays = Query(Play.GET_ALL_QUERY).execute(FetchMode.ALL)

    return jsonify(plays)


@app.get('/play/<int:play_id>')
def get_play(play_id: int):
    play = Query(Play.GET_BY_ID, id=play_id).execute(FetchMode.ONE)
    return jsonify(play)


@app.get('/play/<int:play_id>/students')
def get_play_students(play_id: int):
    students = Query(Student.GET_STUDENTS_BY_PLAY,
                     play_id=play_id).execute(FetchMode.ALL)

    return jsonify(students)


@app.post('/play/<int:play_id>/certificates')
def generate_certificate(play_id: int):
    # if they choose wich students to send the certificate to
    students = request.json

    if not students:
        students_certificate_info = Query(Student.GET_STUDENTS_CERTIFICATE_INFO_BY_PLAY, play_id=play_id)\
            .execute(FetchMode.ALL)
    else:
        students_certificate_info = Query(Student.GET_STUDENTS_CERTIFICATE_INFO_BY_PLAY_AND_CODE,
                                          play_id=play_id,
                                          student_codes=','.join(students)).execute(FetchMode.ALL)

    for student_certificate in students_certificate_info:
        # generar certificado con html

        student_certificate['startDate'] = '{0:%B} de {0:%Y}'.format(
            student_certificate['startDate'])

        student_certificate['endDate'] = '{0:%B} de {0:%Y}'.format(
            student_certificate['endDate'])

        student_render = render_template(
            'certificate.html', **student_certificate)
        student_generated_pdf = html_to_pdf(student_render)

        send_mail(
            to=student_certificate['email'],
            subject='Certificación de la obra {}'.format(
                student_certificate['playTitle']),
            message='',
            attachment_string=student_generated_pdf
        )

    return jsonify({'message': 'Certificates generated successfuly'})


@app.get('/student/<int:code>/plays')
def get_plays_by_student(code: int):
    plays = Query(Play.GET_PLAYS_BY_STUDENT,
                  student_code=code).execute(FetchMode.ALL)

    return jsonify(plays)


@app.post('/login')
def login_professor():
    json_request = request.json
    professor = Query(Employee.GET_BY_DOCUMENT,
                      code=json_request['code']).execute(FetchMode.ONE)
    if professor is not None:
        resp = make_response(
            jsonify({'message': 'OK', 'userId': professor['employeeId']}))
        return resp
    else:
        return jsonify({'message': 'error, Code is not valid'}), 400


@app.get('/allowance/<int:play_id>/students')
def get_allowance_students(play_id: int):
    students = Query(Student.GET_STUDENTS_ALLOWANCE_BY_PLAY,
                     play_id=play_id).execute(FetchMode.ALL)
    res_students = []
    codes = []
    for student in students:
        if not student['code'] in codes:
            codes.append(student['code'])
            temp = {
                'code': student['code'],
                'full_name': student['names'] + " " + student['lastNames'],
                'asistance': []
            }
            for item in students:
                if item['code'] == student['code']:
                    temp['asistance'].append({
                        'type': item['name'],
                        'theater': item['theaterName'],
                        'date': item['date'].strftime("%m/%d/%Y"),
                        'start_time': item['startTime'].strftime("%H:%M:%S"),
                        'end_time': item['endTime'].strftime("%H:%M:%S"),
                    })
            res_students.append(temp)
    return jsonify(res_students)


@app.post('/allowance/<int:play_id>/report')
def generate_report(play_id: int):
    # if they choose wich students to send the certificate to
    request_json = request.json

    students_query = Query(Student.GET_STUDENTS_ALLOWANCE_BY_PLAY,
                     play_id=play_id).execute(FetchMode.ALL)
    students = []
    codes = []
    for student in students_query:
        if not student['code'] in codes:
            codes.append(student['code'])
            temp = {
                'code': student['code'],
                'full_name': student['names'] + " " + student['lastNames'],
                'asistance': []
            }
            for item in students_query:
                if item['code'] == student['code']:
                    temp['asistance'].append({
                        'type': item['name'],
                        'theater': item['theaterName'],
                        'date': item['date'].strftime("%m/%d/%Y"),
                        'start_time': item['startTime'].strftime("%H:%M:%S"),
                        'end_time': item['endTime'].strftime("%H:%M:%S"),
                    })
            students.append(temp)

    professor = Query(Employee.GET_BY_ID, id=request_json['professor_id']).execute(FetchMode.ONE)
    play = Query(Play.GET_BY_ID, id=play_id).execute(FetchMode.ONE)

    student_render = render_template('viaticos.html', professor=professor, students=students, play=play)
    student_generated_pdf = html_to_pdf(student_render, True)
    # response = make_response(student_generated_pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = \
    #     'inline; filename=%s.pdf' % 'report'

    return jsonify({'message': 'Certificates generated successfuly'})


@app.get('/tab/allowance/<int:play_id>')
def get_enabled_allowance_tab(play_id: int):
    active_play = Query(Play.GET_ACTIVE_PLAY_BY_EVENT,
                        id=play_id).execute(fetch=FetchMode.ALL)

    if active_play:
        return jsonify({"active": False})

    return jsonify({"active": True})


def exit_handler():
    Globals.get('connection').close()


atexit.register(exit_handler)


if '__main__':
    app.run()
