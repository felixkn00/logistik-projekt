from flask import jsonify, request
import requests

def refresh_access_token():
    print("run refresh_access_token route")
    refresh_token = request.headers.get('refreshtoken')
    uid = request.headers.get('uid')
    print(refresh_token)
    print(uid)

    error_details = {}
    error_status = False

    if refresh_token is None:
        error_details['refresh_token_empty'] = True
        error_status = True
    if uid is None:
        error_details['uid_empty'] = True
        error_status = True

    if error_status:
        response = {
            "status": "refresh_token_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    url = "http://127.0.0.1:5000/refresh_access_token"
    headers = {
        "refreshtoken": refresh_token,
        "uid": uid
    }

    print("refresh access token route, do request to auth service")
    auth_service_request = requests.post(url, headers=headers)
    if auth_service_request.status_code == 200:
        response_data = auth_service_request.json()
        print(response_data)

        response = {
            "status": "refresh_access_token_successful",
            "new_access_token": response_data['new_access_token'],
        }
        return jsonify(response), auth_service_request.status_code
    else:
        response = {
            "status": "refresh_access_token_failed"
        }
        return jsonify(response), auth_service_request.status_code
