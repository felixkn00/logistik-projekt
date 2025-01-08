from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def put_back_from_scare_commodity_inventory():
    print("run put_back_from_scare_commodity_inventory")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"put_back_from_scare_commodity_inventory: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json
    ItemId = data.get('ItemID')


    error_details = {}
    error_status = False

    # check parameters
    if uid is None:
        error_status = True
        error_details['uid_empty'] = True
    if access_token is None:
        error_status = True
        error_details['access_token_empty'] = True


    # chck if errors
    if error_status:
        error_details['access_token_status'] = True
        response = {
            "status": "put_back_from_scare_commodity_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    response = {}

    # Do auth check
    do_auth = auth(uid, access_token, refresh_token)
    print(do_auth)
    print("put_back_from_scare_commodity_inventory, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "put_back_from_scare_commodity_inventory_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    # create database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        put_back_from_scare_commodity_inventory_query = sql_templates_obj.inventory['put_back_from_scare_commodity_inventory']
        put_back_from_scare_commodity_inventory_data = database.update(put_back_from_scare_commodity_inventory_query, (ItemId,))

        response['status'] = "put_back_from_scare_commodity_inventory_successful"
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "put_back_from_scare_commodity_inventory_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    finally:
        database.close()