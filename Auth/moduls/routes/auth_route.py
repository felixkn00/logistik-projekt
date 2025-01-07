from flask import jsonify, request
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
from mysql.connector import Error
import jwt
import secrets


def auth():
    uid = request.headers.get('uid', None)
    access_token = request.headers.get('accesstoken', None)
    print(access_token)

    error_details = {}
    error_status = False

    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if access_token is None:
        error_status = True
        error_details['access_token'] = True

    if error_status:
        response = {
            "status": "access_token_auth_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        check_token = database.fetch_one(sql_templates_obj.user['check_access_token'], (str(uid), str(access_token)))

        if check_token is None or check_token[0] == 0:
            print("Access Token ist ungültig")
            error_details['token_auth_failed'] = True
            response = {
                "status": "token_auth_failed",
                "errors": error_details
            }
            return jsonify(response), 401

    except Error as e:
        error_details['db_error'] = str(e)
        response = {
            "status": "token_auth_failed",
            "errors": error_details
        }
        print("dbe")
        return jsonify(response), 500

    try:
        secret_key = secrets.token_hex(32)
        access_token = jwt.encode({}, secret_key, algorithm='HS256', headers={'alg': 'HS256', 'typ': 'JWT'})
        print("Neuer Token generiert:", access_token)

        update_result = database.update(sql_templates_obj.user['update_access_token'], (str(access_token), str(uid)))

        response = {
            "status": "access_token_auth_successful",
            "new_access_token": access_token
        }
        return jsonify(response), 200

    except Error as e:
        error_details['db_error'] = str(e)
        response = {
            "status": "access_token_auth_failed",
            "errors": error_details
        }

        return jsonify(response), 500

    finally:
        database.close()
