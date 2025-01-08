from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates


def add_scare_commodity_inventory():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"Get add_scare_commodity_from_inventory: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json
    ItemID = data.get('ItemID')

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
            "status": "move_to_scare_commodity_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("add_scare_commodity_inventory, auth check")

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
        query = sql_templates_obj.inventory['move_to_scarce_commodity_inventory']
        data = database.update(query, (ItemID,))
        print(f"data: {data}")

        show_item_availability_query = sql_templates_obj.inventory['select_item_by_ItemID']
        show_item_availability_data = database.fetch_one(show_item_availability_query, (ItemID,))
        print(f"show_item_availability_data: {show_item_availability_data}")

        if show_item_availability_data and show_item_availability_data[0] > 0:

            show_if_inside_scare_commodity_query = sql_templates_obj.scare_commodity_inventory['show_if_item_is_inside']
            show_if_inside_scare_commodity_data = database.fetch_one(show_if_inside_scare_commodity_query, (ItemID,))
            print("show_item_availability_data: true")
            print(show_if_inside_scare_commodity_data)
            if show_if_inside_scare_commodity_data[0] == 0:
                add_to_scare_commodity_query = sql_templates_obj.scare_commodity_inventory['add_scare_commodity_inventory']
                database.insert(add_to_scare_commodity_query, (ItemID, uid))

                print("successful move to scarce commodity")

            else:
                print("already inside scare commodity")
            response['status'] = "move_to_scare_commodity_successful"
            return jsonify(response), 200
        else:
            response['status'] = "move_to_scare_commodity_failed"
            return jsonify(response), 200



    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "move_to_scare_commodity_failed",
            "errors": error_details
        }
        return jsonify(response), 500
