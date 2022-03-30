import cx_Oracle

import config


class Connection:
    def __init__(self) -> None:
        dsn = cx_Oracle.makedsn(
            config.DB_HOST, config.DB_PORT, service_name='XE')

        self.pool = cx_Oracle.SessionPool(
            user=config.DB_USER,
            password=config.DB_PASS,
            dsn=dsn,
            min=100,
            max=100,
            increment=0,
            encoding=config.DB_ENCODING
        )

    def get_connection(self):
        return self.pool.acquire()

    def release_connection(self, connection):
        return self.pool.release(connection)

    def close(self):
        self.pool.close()
