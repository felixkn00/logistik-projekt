from flask import jsonify, request
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
import jwt
import secrets

def login():
    # Get parameter values
    username = request.headers.get('username')
    password = request.headers.get('password')
    print(username)
    print(password)

    error_details = {}
    error_status = False

    if not username:
        error_details['username_empty'] = True
        error_status = True
    if not password:
        error_details['password_empty'] = True
        error_status = True
        print("Password is missing")

    if error_status:
        response = {
            "status": "login_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    # Create Database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        login_query = sql_templates_obj.user['login']
        login_result = database.fetch_one(login_query, (username, password))

        print(login_result)

        if login_result is None:
            print("No result found.")
            response = {
                "status": "login_failed",
                "errors": {"login_gone_wrong": True}
            }
            return jsonify(response), 400

        if isinstance(login_result, tuple):
            user_count = login_result[0]
            if user_count > 0:
                print("Login successful")

                uid_query = sql_templates_obj.user['select_user_by_name']
                uid_result = database.fetch_one(uid_query, (username,))
                print(uid_result)

                if uid_result and isinstance(uid_result, tuple):
                    uid = uid_result[0]
                else:
                    print("UID not found.")
                    response = {
                        "status": "login_failed",
                        "errors": {"uid_not_found": True}
                    }
                    return jsonify(response), 400

                secret_key = secrets.token_hex(32)
                new_access_token = jwt.encode({}, secret_key, algorithm='HS256', headers={'alg': 'HS256', 'typ': 'JWT'})
                new_refresh_token = secrets.token_hex(64)  # Generates a secure random refresh token
                print("new"+new_refresh_token)
                update_query = sql_templates_obj.user['update_tokens']  # This query should update both access and refresh tokens.
                update_result = database.update(update_query, (new_access_token, new_refresh_token, uid))

                if update_result > 0:
                    print("Tokens updated successfully.")
                    response = {
                        "status": "login_successful",
                        "new_access_token": new_access_token,
                        "new_refresh_token": new_refresh_token,  # Return the refresh token to the client
                        "uid": uid
                    }
                    return jsonify(response), 200
                else:
                    error_details["token_update_failed"] = True
                    response = {
                        "status": "login_failed",
                        "errors": error_details
                    }
                    return jsonify(response), 500

            else:
                print("Login failed")
                response = {
                    "status": "login_failed",
                    "errors": {"login_failed": True}
                }
                return jsonify(response), 400

        else:
            print("Unexpected result format.")
            response = {
                "status": "login_failed",
                "errors": {"unexpected_result_format": True}
            }
            return jsonify(response), 400

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "login_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()
