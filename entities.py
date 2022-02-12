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


class Student:
    GET_BY_CODE = """
        select s.*, p.NAMES, p.LAST_NAME, p.EMAIL, p.BIRTH_DATE, c.NAME as CAREER from STUDENT s
        join PERSON p on s.DOC_NUMBER = p.DOC_NUMBER
        join CAREER c on s.CAREER_ID = c.CAREER_ID
        where CODE = :code
    """
