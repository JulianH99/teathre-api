from .globals import Globals
from .utils import camel_clase
from enum import IntEnum, auto


class FetchMode(IntEnum):
    ALL = auto()
    ONE = auto()


class Query:
    def __init__(self, query: str, **params) -> None:
        self.connection = Globals.get('connection').get_connection()
        self.query = query
        self.params = params

    def execute(self, fetch=None):

        with self.connection.cursor() as cur:
            cur.execute(self.query, **self.params)

            if fetch:
                columns = [camel_clase(col[0]) for col in cur.description]
                cur.rowfactory = lambda *args: dict(zip(columns, args))

            if fetch == FetchMode.ALL:
                return cur.fetchall()

            elif fetch == FetchMode.ONE:
                return cur.fetchone()

        self.connection.commit()

        Globals.get('connection').release_connection(self.connection)
