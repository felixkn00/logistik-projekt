from flask import jsonify, request
from moduls.auth import auth
from moduls.database import Database
from moduls.sql_templates import SQLTemplates

def add_delivery_details():
    print("run add delivery details")
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')
    print(f"add delivery details: Token: {access_token}, UID: {uid}, Refresh Token: {refresh_token}")

    data = request.json
    DeliveryID = data.get('DeliveryID')
    Article = data.get('Article')
    Quantity = data.get('Quantity')
    Quantity = int(Quantity)
    SinglePrice = data.get('SinglePrice')
    GraduatedPrice = data.get('GraduatedPrice')


    error_details = {}
    error_status = False


    response = {}

    # do auth check
    do_auth = auth(uid, access_token, None)
    print(do_auth)
    print("add delivery details, auth check")

    if do_auth['status'] == "access_token_auth_failed":
        errors = {
            "token_status": "access_token_auth_failed"
        }
        response['status'] = "add_delivery_details_failed"
        response['errors'] = errors
        return jsonify(response), 400
    response['new_access_token'] = do_auth.get('new_access_token')

    ###
    # add deliveries

    # create database instance
    database = Database(host="localhost", database="logi_connect", user="root", password="")
    sql_templates_obj = SQLTemplates()

    try:
        add_delivery_details_query = sql_templates_obj.deliveries['details']['add_delivery_details']
        add_delivery_details_data = database.insert(add_delivery_details_query, (DeliveryID, Article, Quantity,
                                                                                SinglePrice, GraduatedPrice, uid))
        print(f"add_delivery_details DeliveryItemID: {add_delivery_details_data}")

        response['status'] = "add_delivery_details_successful"
        response['new_DeliveryItemID'] = add_delivery_details_data
        return jsonify(response), 200

    except Exception as e:
        print("Database error:", e)
        error_details['db_error'] = str(e)
        response = {
            "status": "add_delivery_details_failed",
            "errors": error_details
        }
        return jsonify(response), 500

