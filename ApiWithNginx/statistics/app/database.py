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
                                         password=PASSWORD_DB, host=HOST_DB, port=PORT_DB)
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

    def execute_sql(self, sql):
        try:
            self.cursor = self.connect()
            if self.cursor is not None:
                self.cursor.execute(sql)
                response = self.cursor.fetchone()
                return response
        except psycopg2.DatabaseError as e:
            log.error(f"Bad execute to {DBNAME}\nError = {e}\nSQL execute = {sql}")
            return 0

    def create_table_sql(self):
        sql = """CREATE TABLE IF NOT EXISTS users_nosql (
        id serial PRIMARY KEY NOT NULL ,
        data json NOT NULL);"""
        try:
            self.cursor = self.connect()
            if self.cursor is not None:
                self.cursor.execute(sql)
                self.conn.commit()
                return True
        except psycopg2.DatabaseError as e:
            log.error(f"Bad execute to {DBNAME}\nError = {e}\nSQL execute = {sql}")
        finally:
            return False

    def create_table_json(self):
        sql = """CREATE TABLE IF NOT EXISTS users_sql (
id serial PRIMARY KEY NOT NULL ,
email varchar(100) DEFAULT NULL,
username varchar(64) DEFAULT NULL,
name varchar(1000) DEFAULT NULL,
information_bio text DEFAULT NULL,
password varchar(256) DEFAULT NULL
);"""
        try:
            self.cursor = self.connect()
            if self.cursor is not None:
                self.cursor.execute(sql)
                self.conn.commit()
                return True
        except psycopg2.DatabaseError as e:
            log.error(f"Bad execute to {DBNAME}\nError = {e}\nSQL execute = {sql}")
        finally:
            return False

    def count_users_sql(self):
        count,*_ =  self.execute_sql("SELECT COUNT(id) FROM users_sql;")
        return int(count)

    def count_users_json(self):
        count,*_ =  self.execute_sql("SELECT COUNT(id) FROM users_nosql;")
        return int(count)