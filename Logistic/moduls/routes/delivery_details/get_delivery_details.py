from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates


def get_delivery_details():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')

    data = request.get_json()
    DeliveryID = data.get("DeliveryID")
    print(f"Get Delivery Details: Token: {access_token}, UID: {uid}, DID = {DeliveryID}")
    print(DeliveryID)
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
            "status": "get_delivery_details_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("get delivery details, auth check")

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
        get_deliveries_query = sql_templates_obj.deliveries['details']['get_delivery_details']
        deliveries_data = database.fetch_all(get_deliveries_query, (DeliveryID,))
        print(f"__________________{deliveries_data}")
        items = [
            {
                "DeliveryItemID": item[0],
                "DeliveryID": item[1],
                "Article": item[2],
                "Quantity": item[3],
                "SinglePrice": item[4],
                "GraduatedPrice": item[5],
                "UserID": item[6],
                "hasChanged": False,
                "changedFields": {
                    "DeliveryItemID": False,
                    "DeliveryID": False,
                    "Article": False,
                    "Quantity": False,
                    "SinglePrice": False,
                    "GraduatedPrice": False,
                    "UserID": False,
                }
            }
            for item in deliveries_data
        ]
        print(deliveries_data)
        response['status'] = "get_delivery_details_successful"
        response['items'] = items
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "get_delivery_details_failed",
            "errors": error_details
        }
        return jsonify(response), 500
