from flask import jsonify, request
from datetime import datetime
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates
from moduls.permissions import Permissions

def add_user():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"add add_user: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")


    data = request.json
    Username = data.get('Username')
    Password = data.get('Password')
    can_create = int(bool(data.get('can_create', False)))
    can_read = int(bool(data.get('can_read', False)))
    can_update = int(bool(data.get('can_update', False)))
    can_delete = int(bool(data.get('can_delete', False)))
    print(f"can_delete: {can_delete}")

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
            "status": "add_user_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("add user, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "add_user_failed"
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
        print("create permission ok")
        try:
            #show if username is forgiven
            show_if_username_forgiven_query = sql_templates_obj.user['show_if_username_forgiven']
            show_if_username_forgiven_data = database.fetch_one(show_if_username_forgiven_query, (Username,))
            print("show_if_username_forgiven_data: ")
            print(show_if_username_forgiven_data)
            if show_if_username_forgiven_data[0] == 0:

                add_user_query = sql_templates_obj.user['add_user']
                add_user_data = database.insert(add_user_query, (Username, Password, can_create, can_read, can_update, can_delete,))
                print(f"add_user: {add_user_data}")

                response['status'] = "add_user_successful"
                response['new_UserID'] = add_user_data
                return jsonify(response), 200

            else:
                response['status'] = "add_user_username_forgiven"
                return jsonify(response), 200

        except Exception as e:
            print("Database error:", e)
            error_details['db_error'] = str(e)
            response = {
                "status": "add_user_failed",
                "errors": error_details
            }
            return jsonify(response), 500


    else:
        response['status'] = "get_users_failed"
        return jsonify(response)
