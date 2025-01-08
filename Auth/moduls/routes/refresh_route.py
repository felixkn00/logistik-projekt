from flask import jsonify, request
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
from mysql.connector import Error
import jwt
import secrets


def refresh():

    refresh_token = request.headers.get('refreshtoken', None)
    uid = request.headers.get('uid', None)

    error_details = {}
    error_status = False

    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if refresh_token is None:
        error_status = True
        error_details['refresh_token_empty'] = True

    if error_status:
        response = {
            "status": "refresh_token_auth_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:

        check_refresh_token = database.fetch_one(sql_templates_obj.user['check_refresh_token'],
                                                 (str(uid), str(refresh_token)))

        if check_refresh_token is None or check_refresh_token[0] == 0:
            error_details['invalid_refresh_token'] = True
            response = {
                "status": "refresh_token_auth_failed",
                "errors": error_details
            }
            return jsonify(response), 401

        secret_key = secrets.token_hex(32)
        new_access_token = jwt.encode({}, secret_key, algorithm='HS256', headers={'alg': 'HS256', 'typ': 'JWT'})
        print("Neues Zugriffstoken generiert:", new_access_token)

        update_result = database.update(sql_templates_obj.user['update_access_token'],
                                        (str(new_access_token), str(uid)))

        response = {
            "status": "refresh_token_auth_successful",
            "new_access_token": new_access_token
        }
        return jsonify(response), 200

    except Error as e:
        error_details['db_error'] = str(e)
        response = {
            "status": "refresh_token_auth_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()
