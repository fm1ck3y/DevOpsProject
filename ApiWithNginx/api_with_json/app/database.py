import psycopg2
import os
import logging

log = logging.getLogger(__name__)

DBNAME = os.getenv('POSTGRES_DB')
USER_DB = os.getenv('POSTGRES_USER')
PASSWORD_DB = os.getenv('POSTGRES_PASSWORD')
HOST_DB = os.getenv('POSTGRES_HOST')
PORT_DB = os.getenv('POSTGRES_PORT')

class Database:
    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=DBNAME, user=USER_DB,
                                password=PASSWORD_DB, host=HOST_DB,port = PORT_DB)
            if self.conn is not None:
                logging.debug(f"Good connection to {DBNAME} with host= {HOST_DB}")
                self.create_table()
                return self.conn.cursor()
            raise psycopg2.DatabaseError
        except psycopg2.DatabaseError as e:
            log.info(f"Bad connection to {DBNAME} with host = {HOST_DB}. Error - {e}")
            log.info(self.conn)
            return None

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            log.debug(f"Bad close connection to {DBNAME}")

    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS users_nosql (
id serial PRIMARY KEY NOT NULL ,
data json NOT NULL);"""
        self.execute_sql(sql)

    def execute_sql(self,sql):
        result = False
        try:
            self.cursor = self.connect()
            if self.cursor is not None:
                self.cursor.execute(sql)
                self.conn.commit()
                result = True
        except psycopg2.DatabaseError as e:
            log.error(f"Bad execute to {DBNAME}\nError = {e}\nSQL execute = {sql}")
        finally:
            return result

    def add_user(self,user):
        sql = f"INSERT INTO users_nosql (data) " \
              f"VALUES ('{user}');"
        return self.execute_sql(sql)