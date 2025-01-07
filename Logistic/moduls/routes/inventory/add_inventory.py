from flask import jsonify, request
from datetime import datetime
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def add_inventory():
    print("run add inventory")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"Add Inventory: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json

    ItemNumber = data.get('ItemNumber')
    ItemName = data.get('ItemName')
    Category = data.get('Category')
    StockQuantity = data.get('StockQuantity')
    SinglePrice = data.get('SinglePrice')
    GraduatedPrice = data.get('GraduatedPrice')
    ExpiryDate = data.get('ExpiryDate') or datetime.now().date()


    error_details = {}
    error_status = False

    #check parameters

    response = {}

    # Do auth check
    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("add inventory, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "add_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    ###
    # add inventory

    # create database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        add_inventory_item_query = sql_templates_obj.inventory['add_inventory']
        add_inventory_item_data = database.insert(add_inventory_item_query, (ItemNumber, ItemName, Category,
                                                        StockQuantity, SinglePrice, GraduatedPrice, ExpiryDate, uid))
        print(f"add_inventory newItem: {add_inventory_item_data}")

        response['status'] = "add_inventory_successful"
        response['new_ItemID'] = add_inventory_item_data
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "add_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 500

