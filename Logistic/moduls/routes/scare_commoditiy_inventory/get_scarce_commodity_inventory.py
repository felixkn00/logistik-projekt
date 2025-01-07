from flask import jsonify, request
from datetime import datetime
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates


def get_scarce_commodity_inventory():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"get_scarce_commodity_inventory: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

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
            "status": "get_scarce_commodity_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("get_scarce_commodity_inventory, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "get_scare_commodity_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        get_scare_commodity_inventory_query = sql_templates_obj.scare_commodity_inventory['get_inventory']
        get_scare_commodity_inventory_data = database.fetch_all(get_scare_commodity_inventory_query)
        print(f"get_scarce_commodity_inventory_data, result: {get_scare_commodity_inventory_data}")
        items = [
            {
                "ItemID": item[0],
                "ItemNumber": item[1],
                "ItemName": item[2],
                "StockQuantity": item[3],
                "Category": item[4],
                "SinglePrice": item[5],
                "GraduatedPrice": item[6],
                "ExpiryDate": item[7].strftime("%Y-%m-%d") if item[7] is not None else None,
                "UserID": item[8],
                "StorageID": item[9],
                "Donated": item[10],
                "ThrownAway": item[11],
                "Returned": item[12],
                "Repaired": item[13],
                "UserID_ScarceCommodity": item[14],
                "hasChanged": False,
                "changedFields": {
                    "ItemID": False,
                    "ItemNumber": False,
                    "ItemName": False,
                    "Category": False,
                    "SinglePrice": False,
                    "GraduatedPrice": False,
                    "ExpiryDate": False,
                    "UserID": False,
                    "StorageID": False,
                    "Donated": False,
                    "ThrownAway": False,
                    "Returned": False,
                    "Repaired": False
                }
            }
            for item in get_scare_commodity_inventory_data
        ]

        response['status'] = "get_scarce_commodity_inventory_successful"
        response['items'] = items
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "get_scarce_commodity_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 500
