import logging
import mysql.connector
from mysql.connector import Error
from sql_templates import SQLTemplates


# Database Class
class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()

        except Error:
            return Error

    def query(self, sql, params=None):

        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except Error:
            self.connection.rollback()
            return Error

    def fetch_one(self, sql, params=None):
        try:
            self.query(sql, params)
            return self.cursor.fetchone()
        except Error:
            return Error

    def fetch_all(self, sql, params=None):
        try:
            self.query(sql, params)
            return self.cursor.fetchall()
        except Error:
            return Error

    def insert(self, sql, params):
        try:
            self.query(sql, params)
            return self.cursor.lastrowid
        except Error:
            return Error

    def close(self):
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
        except Error:
            return Error


#Logger Class

class Logger:
    def __init__(self):
        self.database = Database(host="localhost", database="logger_store", user="root", password="")
        self.SQL_templates_obj = SQLTemplates

    def system_error(self, error, location, description):
        if error != "":

            try:
                self.database.insert(self.SQL_templates_obj.logger['database']["insert_database_error"], "%s%s%s")
            except Error:
                print("Failed to insert Error")

    def user_action(self, action, uid, location, description):
        if action != "" and uid != "":
            try:
                self.database.insert(self.SQL_templates_obj.logger['user']['insert_user_action'], "%s%i")
            except Error:
                print("Failed by inserting User Action")