from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates


def update_scarce_commodity_inventory():
    print("run update_scarce_commodity_inventory")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"update_scarce_commodity_inventory: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json
    ItemID = data.get('ItemID') if data.get('ItemID') else None
    print(f"Data: {ItemID}")
    ItemNumber = data.get('ItemNumber') if data.get('ItemNumber') else None
    ItemName = data.get('ItemName') if data.get('ItemName') else None
    StockQuantity = data.get('StockQuantity') if data.get('StockQuantity') else None
    Category = data.get('Category') if data.get('Category') else None
    SinglePrice = data.get('SinglePrice') if data.get('SinglePrice') else None
    GraduatedPrice = data.get('GraduatedPrice') if data.get('GraduatedPrice') else None
    ExpiryDate = data.get('ExpiryDate') if data.get('ExpiryDate') else None
    StorageID = data.get('StorageID') if data.get('StorageID') else None
    Donated = data.get('Donated') if data.get('Donated') else None
    ThrownAway = data.get('ThrownAway') if data.get('ThrownAway') else None
    Returned = data.get('Returned') if data.get('Returned') else None
    Repaired = data.get('Repaired') if data.get('Repaired') else None


    error_details = {}
    error_status = False

    # check parameters
    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if access_token is None:
        error_status = True
        error_details['access_token_empty'] = True

    # check if errors
    if error_status:
        error_details['access_token_status'] = True
        response = {
            "status": "update_scarce_commodity_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    # Do auth check
    do_auth = auth(uid, access_token, refresh_token)
    print(do_auth)
    print("update_scarce_commodity_inventory, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "update_scarce_commodity_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    # create database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        update_scarce_commodity_inventory_query = sql_templates_obj.scare_commodity_inventory['update_scarce_commodity_inventory']
        update_scarce_commodity_inventory_data = database.update(update_scarce_commodity_inventory_query, (
            ItemNumber, ItemName, Category, StockQuantity, SinglePrice, GraduatedPrice, ExpiryDate, uid, Donated,
            ThrownAway, Returned, Repaired, uid, ItemID))
        print(update_scarce_commodity_inventory_data)
        print(update_scarce_commodity_inventory_query)
        print(update_scarce_commodity_inventory_data)

        response['status'] = "update_scarce_commodity_inventory_successful"
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "update_scarce_commodity_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()
