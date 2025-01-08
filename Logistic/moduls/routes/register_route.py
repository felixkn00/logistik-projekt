from flask import jsonify, request
import requests


def register():
    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)

    error_details = {}
    error_status = None

    if username is None:
        error_details['username_empty'] = True
        error_status = True
    if password is None:
        error_details['password_empty'] = True
        error_status = True

    if error_status is True:
        response = {
            "status": "registration_failed",
            "errors": error_details
        }
        return jsonify(response), 500

    url = "http://127.0.0.1:5000/register"

    # create request
    request_parameter = {
        "username": username,
        "password": password
    }

    # do request to auth service
    auth_service_request = requests.post(url, headers=request_parameter)

    if auth_service_request.status_code == 200:
        response = {
            "status": "register_successful"
        }
        return jsonify(response), 200
    else:
        response = {
            "status:" "register_failed"
        }
        return jsonify(response), auth_service_request.status_code
