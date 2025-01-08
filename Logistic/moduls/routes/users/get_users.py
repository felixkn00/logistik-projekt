from flask import jsonify, request
from datetime import datetime
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
from moduls.permissions import Permissions

def get_users():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"get_users: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")


    error_details = {}
    error_status = False

    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if access_token is None:
        error_status = True
        error_details['access_token_empty'] = True

    if error_status:
        error_details['access_token_status'] = True
        response = {
            "status": "get_items_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token,   None)
    print(do_auth)
    print("get inventory, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "get_users_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    ##
    # Check Permissions
    permissions = Permissions(uid)

    all_permissions = permissions.get_all()

    if all_permissions['superuser'] == 1:
        database = Database(host="localhost", database="logi_connect", user="root", password="")
        sql_templates_obj = SQLTemplates()

        try:
            get_users_query = sql_templates_obj.user['get_users']
            users_data = database.fetch_all(get_users_query)
            print(f"__________________{users_data}")
            items = [
                {
                    "UserID": item[0],
                    "Username": item[1],
                    "Password": item[2],
                    "Email": item[3],
                    "can_create": item[6],
                    "can_read": item[7],
                    "can_update": item[8],
                    "can_delete": item[9],
                    "isSuperuser": item[10],
                    "hasChanged": False,
                    "changedFields": {
                        "UserID": False,
                        "Username": False,
                        "Password": False,
                        "Email": False,
                        "can_create": False,
                        "can_read": False,
                        "can_update": False,
                        "can_delete": False
                    }
                }
                for item in users_data
            ]

            response['status'] = "get_users_successful"
            response['items'] = items
            return jsonify(response), 200

        except Exception as e:
            print("Database error:", e)
            error_details['db_error'] = str(e)
            response = {
                "status": "get_users_failed",
                "errors": error_details
            }
            return jsonify(response), 500

    else:
        response['status'] = "get_users_failed"
        return jsonify(response)
