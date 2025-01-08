from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def get_deliveries():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"get deliveries: token: {access_token}, uid: {uid}, tefresh token: {refresh_token}")

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
            "status": "get_deliveries_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("get deliveries, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        print("access_token_auth_failed")
        response['status'] = "get_items_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        get_deliveries_query = sql_templates_obj.deliveries['get_deliveries']
        deliveries_data = database.fetch_all(get_deliveries_query)
        print(f"__________________{deliveries_data}")
        items = [
            {
                "DeliveryID": item[0],
                "DeliveryNumber": item[1],
                "SupplierName": item[2],
                "Information": item[3],
                "Price": item[4],
                "DeliveryStatus": item[5],
                "DeliveryDate": item[6].strftime("%Y-%m-%d"),
                "UserID": item[7],
                "hasChanged": False,
                "changedFields": {
                    "DeliveryID": False,
                    "DeliveryNumber": False,
                    "SupplierName": False,
                    "Information": False,
                    "Price": False,
                    "DeliveryStatus": False,
                    "DeliveryDate": False,
                    "UserID": False
                }
            }
            for item in deliveries_data
        ]
        print(deliveries_data)
        response['status'] = "get_deliveries_successful"
        response['items'] = items
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "get_deliveries_failed",
            "errors": error_details
        }
        return jsonify(response), 500
