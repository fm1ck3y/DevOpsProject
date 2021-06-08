import psycopg2
import os
import logging

log = logging.getLogger(__name__)

DBNAME = os.getenv('DBNAME')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')

class Database:
    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=DBNAME, user=USER_DB,
                                password=PASSWORD_DB, host=HOST_DB,port = PORT_DB)
            if self.conn is not None:
                logging.debug(f"Good connection to {DBNAME} with host= {HOST_DB}")
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
            self.close_connection()
            return result

    def add_user(self,email,username,full_name,information_bio,password):
        sql = f"INSERT INTO users (email,username,name,information_bio,password) " \
              f"VALUES ('{email}','{username}','{full_name}','{information_bio}','{password}');"
        return self.execute_sql(sql)