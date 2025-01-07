from flask import jsonify, request
from datetime import datetime
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def update_deliveries():
    print("run update deliveries")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"Update Deliveries: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json
    DeliveryID = data.get('DeliveryID')
    print(f"Data: {DeliveryID}")
    DeliveryNumber = data.get('DeliveryNumber')
    SupplierName = data.get('SupplierName')
    Information = data.get('Information')
    Price = data.get('Price')
    DeliveryStatus = data.get('DeliveryStatus')
    DeliveryDate = data.get('DeliveryDate') or datetime.now().date()
    print(DeliveryDate)


    error_details = {}
    error_status = False

    # Check parameters
    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if access_token is None:
        error_status = True
        error_details['access_token_empty'] = True


    # check if error by parameters
    if error_status:
        error_details['access_token_status'] = True
        response = {
            "status": "update_deliveries_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    # Do auth check
    do_auth = auth(uid, access_token, refresh_token)
    print(do_auth)
    print("get inventory, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "update_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    # update deliveries

    # create database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        update_deliveries_query = sql_templates_obj.deliveries['update_deliveries']
        update_deliveries_result = database.update(update_deliveries_query, (DeliveryNumber, SupplierName, Information, Price, DeliveryStatus, DeliveryDate, uid, DeliveryID))
        print(update_deliveries_result)

        response['status'] = "update_deliveries_successful"
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "update_deliveries_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()