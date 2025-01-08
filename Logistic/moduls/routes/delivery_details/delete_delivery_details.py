from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def delete_delivery_details():
    print("run delete delivery details")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')

    print(f"Delete delivery Details: Token: {access_token}, UID: {uid}")

    data = request.json
    DeliveryItemID = data.get('DeliveryItemID')

    error_details = {}
    error_status = False

    # check parameters
    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if access_token is None:
        error_status = True
        error_details['access_token_empty'] = True

    # check if error
    if error_status:
        error_details['access_token_status'] = True
        response = {
            "status": "delete_delivery_details_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    # Do auth check
    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("delete delivery details, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "update_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    # delete delivery details

    # Create Database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        delete_deliveries_query = sql_templates_obj.deliveries['details']['delete_delivery_details']
        delete_deliveries_result = database.update(delete_deliveries_query, (DeliveryItemID,))
        print(delete_deliveries_result)

        response['status'] = "delete_delivery_details_successful"
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "delete_delivery_details_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()