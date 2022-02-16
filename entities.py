class Play:
    GET_ALL_QUERY = """
        SELECT PLAY.*, pt.name as PLAY_TYPE, c.NAME as country from PLAY
        join PLAY_TYPE pt on PLAY.PLAY_TYPE_ID = pt.PLAY_TYPE_ID
        join COUNTRY c on PLAY.COUNTRY_CODE = c.CODE
    """

    GET_PLAYS_BY_STUDENT_CONVOCATION = """
        select p.*, pt.NAME as play_type, co.NAME as country from PLAY p
        join COUNTRY co on co.CODE = p.COUNTRY_CODE
        join PLAY_TYPE pt on pt.PLAY_TYPE_ID = p.PLAY_TYPE_ID
        join CONVOCATION c on c.PLAY_ID = p.PLAY_ID
        join CONVOCATION_APPLICANT ca on ca.CONVOCATION_ID = c.ID
        where ca.STUDENT_CODE = :code
    """


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
    SAVE_NEW = """insert into CONVOCATION_APPLICANT (convocation_id, student_code, doc_number)
        values (:convocation_id, :student_code, :doc_number)"""


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


class DocumentType:
    GET_ALL = """
        select * from DOCUMENT_TYPE
    """


class Career:
    GET_ALL = """
        select * from CAREER
    """
