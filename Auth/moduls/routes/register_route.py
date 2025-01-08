from flask import jsonify, request
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
from mysql.connector import Error


def register():
    # get parameter values
    creator_id = request.headers.get('creator_id', None)
    username = request.headers.get('username', None)
    password = request.headers.get('password', None)

    error_details = {}
    error_status = None

    response = {}

    if username is None:
        error_details['username_empty'] = True
        error_status = True
    if password is None:
        error_details['password_empty'] = True
        error_status = True

    if error_status is True:
        response = {
            "status": "registration_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    # create Database Inst.
    database = Database(host="localhost", database="logger_store", user="root", password="")
    sql_templates_obj = SQLTemplates

    # show if user already exists
    try:
        user_exists_result = database.fetch_one(sql_templates_obj.user['select_user_with_username'], (username))

        if user_exists_result:
            response = {
                "status": "registration_failed",
                "errors": {"username_already_exists": True}
            }
            return jsonify(response), 400

    except Error as e:
        error_details['db_error'] = str(e)
        response = {
            "status": "registration_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    # add user into database
    try:
        insert_user = database.insert(sql_templates_obj.user['insert_user'], (creator_id, username, password))

        if insert_user:
            response = {
                "status": "registration_successful",
                "user_id": insert_user
            }
            return jsonify(response), 201
        else:

            error_details['db_insert_user']: True

            response = {
                "status": "registration_failed",
                "errors": error_details
            }
            return jsonify(response), 400

    except Error as e:
        error_details['db_error'] = str(e)
        response = {
            "status": "registration_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()
