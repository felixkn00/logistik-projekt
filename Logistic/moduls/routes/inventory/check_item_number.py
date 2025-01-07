from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates


def check_item_number():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    data = request.json
    ItemNumber = data.get('ItemNumber')
    print(ItemNumber)


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
            "status": "check_item_number_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("inventory - check item number, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "check_item_number_forgiven"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    # Create database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:

        check_item_number_query = sql_templates_obj.inventory['check_item_number']
        check_item_number_query_result = database.fetch_one(check_item_number_query, (ItemNumber,))

        if check_item_number_query_result is None:
            print("No Result ")
            response = {
                "status": "login_failed",
                "errors": {"check_item_number_failed": True}
            }
            return jsonify(response), 400

        if isinstance(check_item_number_query_result, tuple):
            item_number_count = check_item_number_query_result[0]
            if item_number_count == 0:
                response['status'] = "item_number_is_free"
                response['forItemNumber'] = ItemNumber
                return jsonify(response), 200
            else:
                response['status'] = "item_number_is_forgiven"
                response['forItemNumber'] = ItemNumber
                return jsonify(response), 200

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