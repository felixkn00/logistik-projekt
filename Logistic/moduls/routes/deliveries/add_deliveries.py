from flask import jsonify, request
from datetime import datetime
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def add_deliveries():
    print("run add inventory")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"Add Inventory: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json

    DeliveryNumber = data.get('DeliveryNumber')
    SupplierName = data.get('SupplierName')
    Information = data.get('Information')
    Price = data.get('Price')
    if Price is None or Price == '':
        Price = 0.0
    DeliveryStatus = data.get('DeliveryStatus')
    DeliveryDate = data.get('DeliveryDate') or datetime.now().date()

    error_details = {}
    error_status = False


    #check parameters

    response = {}

    # Do auth check
    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("add deliveries, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "update_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    ###
    # Add deliverie to database

    # Create Database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        add_deliveries_item_query = sql_templates_obj.deliveries['add_deliveries']
        add_deliveries_item_data = database.insert(add_deliveries_item_query, (DeliveryNumber, SupplierName, Information, Price, DeliveryStatus, DeliveryDate, uid,))

        print(f"add_deliveries add_deliveries_item_data: {add_deliveries_item_data}")

        response['status'] = "add_deliveries_successful"
        response['new_DeliveryID'] = add_deliveries_item_data
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "add_delivery_failed",
            "errors": error_details
        }
        return jsonify(response), 500

