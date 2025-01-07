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
                print("Connection failed.")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
        except Error as e:
            print(f"Error executing query: {e}")
            return e

    def fetch_one(self, sql, params=None):
        try:
            self.query(sql, params)
            result = self.cursor.fetchone()
            if result is None:
                print("No rows returned.")
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return e

    def fetch_all(self, sql, params=None):
        try:
            self.query(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return e

    def insert(self, sql, params):
        try:
            self.query(sql, params)
            self.connection.commit()  # Commit transaction
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()  # Rollback in case of error
            print(f"Error inserting data: {e}")
            return e

    def update(self, sql, params):
        try:
            self.query(sql, params)
            self.connection.commit()  # Commit transaction
            return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()  # Rollback in case of error
            print(f"Error updating data: {e}")
            return e

    def close(self):
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
        except Error as e:
            print(f"Error closing connection: {e}")