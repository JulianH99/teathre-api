class Play:
    GET_ALL_QUERY = """
        SELECT PLAY.*, pt.name as PLAY_TYPE, c.NAME as country from PLAY
        join PLAY_TYPE pt on PLAY.PLAY_TYPE_ID = pt.PLAY_TYPE_ID
        join COUNTRY c on PLAY.COUNTRY_CODE = c.CODE
        where PLAY.STATE = :state
    """

    GET_PLAYS_BY_STUDENT_CONVOCATION = """
        select p.*, pt.NAME as play_type, co.NAME as country, pc.NAME, pc.name as character, ca.AUDITION_DATE  from PLAY p
        join COUNTRY co on co.CODE = p.COUNTRY_CODE
        join PLAY_TYPE pt on pt.PLAY_TYPE_ID = p.PLAY_TYPE_ID
        join CONVOCATION c on c.PLAY_ID = p.PLAY_ID
        join CONVOCATION_APPLICANT ca on ca.CONVOCATION_ID = c.ID
        join PLAY_CHARACTER pc on pc.PLAY_CHARACTER_ID = ca.CHARACTER_ID
        where ca.STUDENT_CODE = :code
    """

    GET_BY_ID = """
        select * from play where play_id = :id
    """
    GET_ACTIVE_PLAY_BY_TEACHER = """
        select P.PLAY_ID, P.TITLE, P.PLAY_DATE, PA.PLAY_EVENT_ID, PE.START_TIME, PE.END_TIME
        from EMPLOYEE
                join PLAY_PARTICIPANT PP on EMPLOYEE.EMPLOYEE_ID = PP.EMPLOYEE_ID and EMPLOYEE.UNIT_ID = PP.UNIT_ID
                join PLAY_ACTIVITY PA
                    on PP.PARTICIPANT_ID = PA.PARTICIPANT_ID and PP.EMPLOYEE_ID = PA.EMPLOYEE_ID and PP.UNIT_ID = PA.UNIT_ID
                join PLAY P on PA.PLAY_ID = P.PLAY_ID
                join PLAY_EVENT PE on P.PLAY_ID = PE.PLAY_ID
        where TO_CHAR(PE.START_TIME, 'HH24:MI:SS') <= TO_CHAR(sysdate, 'HH24:MI:SS')
        and TO_CHAR(PE.END_TIME, 'HH24:MI:SS') >= TO_CHAR(sysdate, 'HH24:MI:SS')
        and TO_CHAR(PE."date", 'YYYY-MM-DD') = TO_CHAR(sysdate, 'YYYY-MM-DD')
        and EMPLOYEE.EMPLOYEE_ID = :employee_id
        and P.PLAY_ID = :play_id
    """

    GET_PLAYS_BY_STUDENT = """
        select P.PLAY_ID, P.TITLE, PC.NAME as CHARACTER, S.CODE as STUDENT_CODE from PLAY P
        join PLAY_CHARACTER PC on P.PLAY_ID = PC.PLAY_ID
        join STUDENT_CHARACTER SC on PC.ID = SC.CHARACTER_ID and PC.PLAY_ID = SC.PLAY_ID
        join STUDENT S on SC.STUDENT_CODE = S.CODE
        where SC.STUDENT_CODE = :student_code
    """


class Character:
    GET_CHARACTERS = """select * from play_character where play_id = :play_id"""
    GET_BY_ID = """select name from play_character where play_character_id = :id"""


class Person:
    GET_BY_DOC = """
        select * from PERSON where doc_number = :doc_number
    """

    SAVE_NEW = """
        insert into PERSON (DOC_NUMBER, DOCUMENT_TYPE_ID, NAMES, LAST_NAME, BIRTH_DATE, EMAIL)
            values (:doc_number, :document_type_id, :names, :last_name, to_date(:birth_date,'YYYY-MM-DD'), :email)
    
    """


class Convocation:
    CHECK_BY_PLAY = "select * from CONVOCATION where play_id = :play_id and sysdate between start_date and end_date"


class ConvocationApplicant:
    SAVE_NEW = """insert into CONVOCATION_APPLICANT (convocation_id, student_code, doc_number, character_id, audition_date)
        values (:convocation_id, :student_code, :doc_number, :character_id, TO_DATE(:audition_date, 'YYYY-MM-DD'))"""

    GET_APPLICATION = """select * from convocation_applicant where 
        doc_number = :doc_number 
        and student_code = :student_code 
        and convocation_id = :convocation
        and character_id = :character"""


class ConvocationDates:
    GET_BY_CONVOCATION = """select available_date from convocation_dates where convocation_id = :id"""


class Student:
    GET_BY_CODE = """
        select s.*, p.NAMES, p.LAST_NAME, p.EMAIL, p.BIRTH_DATE, c.NAME as CAREER from STUDENT s
        join PERSON p on s.DOC_NUMBER = p.DOC_NUMBER
        join CAREER c on s.CAREER_ID = c.CAREER_ID
        where CODE = :code
    """

    CHECK_BY_CODE = """ select * from STUDENT where CODE = :code """

    SAVE_NEW = """
        insert into STUDENT (doc_number, code, career_id)
            values (:doc_number, :code, :career_id)
    """

    GET_STUDENTS_APPLIED_TO_PLAY = """
        select s.code, c2.name as career, p2.* from student s
        join career c2 on c2.career_id  = s.career_id 
        join person p2 on p2.doc_number  = s.doc_number 
        join convocation_applicant ca on s.doc_number = ca.doc_number and ca.student_code = s.code  
        join convocation c  on ca.convocation_id  = c.id 
        join play p on c.play_id  = p.play_id 
        where p.play_id = :play_id
    """

    GET_STUDENTS_BY_PLAY = """
        select STUDENT.CODE, STUDENT.NAMES, STUDENT.LAST_NAMES, PC.NAME as CHARACTER from STUDENT
        join STUDENT_CHARACTER on STUDENT.CODE = STUDENT_CHARACTER.STUDENT_CODE
        join PLAY_CHARACTER PC on STUDENT_CHARACTER.CHARACTER_ID = PC.ID and STUDENT_CHARACTER.PLAY_ID = PC.PLAY_ID
        join PLAY P on PC.PLAY_ID = P.PLAY_ID
        where P.PLAY_ID = :play_id
    """

    GET_STUDENTS_BY_PLAY_ASSISTANCE = """
        select STUDENT.CODE, STUDENT.NAMES, STUDENT.LAST_NAMES, PC.NAME as CHARACTER, count(SA.PLAY_ID) ASSISTANCE from STUDENT
        join STUDENT_CHARACTER on STUDENT.CODE = STUDENT_CHARACTER.STUDENT_CODE
        join PLAY_CHARACTER PC on STUDENT_CHARACTER.CHARACTER_ID = PC.ID and STUDENT_CHARACTER.PLAY_ID = PC.PLAY_ID
        join PLAY P on PC.PLAY_ID = P.PLAY_ID
        join PLAY_EVENT PE on PE.PLAY_ID = P.PLAY_ID
        left join STUDENT_ASISTANCE SA on STUDENT.CODE = SA.STUDENT_CODE and SA.PLAY_ID = P.PLAY_ID and SA.PLAY_EVENT_ID = PE.PLAY_EVENT_ID
        where P.PLAY_ID = :play_id and PE.PLAY_EVENT_ID = :play_event_id
        group by STUDENT.CODE, STUDENT.NAMES, STUDENT.LAST_NAMES, PC.NAME
    """

    GET_STUDENTS_CERTIFICATE_INFO_BY_PLAY = """
        select ST.CODE, ST.NAMES, ST.LAST_NAMES, ST.EMAIL, P.TITLE as PLAY_TITLE,
        (select min(PE."date") from PLAY_EVENT PE
            join STUDENT_ASISTANCE SA on PE.PLAY_EVENT_ID = SA.PLAY_EVENT_ID and PE.PLAY_ID = SA.PLAY_ID
        where PE.PLAY_ID = P.PLAY_ID
            and SA.STUDENT_CODE = ST.CODE) as START_DATE,
        (select max(PE."date") from PLAY_EVENT PE
            join STUDENT_ASISTANCE SA on PE.PLAY_EVENT_ID = SA.PLAY_EVENT_ID and PE.PLAY_ID = SA.PLAY_ID
        where PE.PLAY_ID = P.PLAY_ID
            and SA.STUDENT_CODE = ST.CODE) as END_DATE,
            PC.NAME as CHARACTER
        from STUDENT ST
        join STUDENT_CHARACTER SC on ST.CODE = SC.STUDENT_CODE
        join PLAY_CHARACTER PC on SC.CHARACTER_ID = PC.ID and SC.PLAY_ID = PC.PLAY_ID
        join PLAY P on PC.PLAY_ID = P.PLAY_ID
        where P.PLAY_ID = :play_id
    """

    GET_STUDENTS_CERTIFICATE_INFO_BY_PLAY_AND_CODE = f"""
        {GET_STUDENTS_CERTIFICATE_INFO_BY_PLAY}
        and ST.CODE in (:student_codes)
    """


class Employee:
    GET_BY_DOCUMENT = """
        SELECT E.EMPLOYEE_ID, NAMES, LAST_NAMES, ID_NUMBER, PHONE_NUMBER, EMAIL from EMPLOYEE E
        where E.ID_NUMBER = :code
    """


class DocumentType:
    GET_ALL = """
        select * from DOCUMENT_TYPE
    """


class Career:
    GET_ALL = """
        select * from CAREER
    """


class StudentAssistance:
    SAVE_NEW_ASSISTANCE = """INSERT INTO STUDENT_ASISTANCE(PLAY_EVENT_ID, PLAY_ID, STUDENT_CODE)
        VALUES (:play_event_id, :play_id, :student_code)"""

    GET_ASSISTANCE = """
        Select STUDENT_ASISTANCE_ID from STUDENT_ASISTANCE WHERE STUDENT_CODE = :student_code
        and PLAY_EVENT_ID = :play_event_id and PLAY_ID = :play_id
    """
