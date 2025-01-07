import mysql.connector
from mysql.connector import Error

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
            else:
                print("connection failed")
        except Error as e:
            print(f"error by connecting to mysql server: {e}")

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
        except Error as e:
            print(f"error exec by query {e}")
            return e

    def fetch_one(self, sql, params=None):
        try:
            self.query(sql, params)
            result = self.cursor.fetchone()
            if result is None:
                print("No rows")
            return result
        except Error as e:
            print(f"error by fetching data: {e}")
            return e

    def fetch_all(self, sql, params=None):
        try:
            self.query(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"error by fetching data: {e}")
            return e

    def insert(self, sql, params):
        try:
            self.query(sql, params)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"error inserting data: {e}")
            return e

    def update(self, sql, params):
        try:
            self.query(sql, params)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            print(f"error updating data: {e}")
            return e

    def close(self):
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
        except Error as e:
            print(f"error by closing connection: {e}")