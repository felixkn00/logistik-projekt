from flask import jsonify, request
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
import jwt
import secrets

def refresh_access_token():
    refresh_token = request.headers.get('refreshtoken')
    uid = request.headers.get('uid')
    print(refresh_token)
    print(uid)

    error_details = {}
    error_status = False

    if refresh_token is None:
        error_details['refresh_access_token_empty'] = True
        error_status = True
    if uid is None:
        error_details['uid_empty'] = True
        error_status = True

    if error_status:
        response = {
            "status": "refresh_access_token_failed",
            "errors": error_details
        }
        return jsonify(response), 400


    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        check_refresh_token_query = sql_templates_obj.user['check_refresh_token']
        check_result = database.fetch_one(check_refresh_token_query, (uid, refresh_token))

        if check_result is None:
            print("No result found.")
            response = {
                "status": "refresh_access_token_failed",
                "errors": {"refresh_access_token_failed": True}
            }
            return jsonify(response), 400
    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "refresh_access_token_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    try:
        new_access_token = secrets.token_hex(64)
        print("new" + new_access_token)
        update_query = sql_templates_obj.user['update_refresh_access_token']
        update_result = database.update(update_query, (new_access_token, uid))

        if update_result > 0:
            print("Tokens updated successfully.")
            response = {
                "status": "refresh_access_token_successful",
                "new_access_token": new_access_token
            }
            return jsonify(response), 200
        else:
            error_details["token_update_failed"] = True
            response = {
                "status": "refresh_access_token_failed",
                "errors": error_details
            }
            return jsonify(response), 500
    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "refresh_access_token_failed",
            "errors": error_details
        }
        return jsonify(response), 500



    finally:
        database.close()
 