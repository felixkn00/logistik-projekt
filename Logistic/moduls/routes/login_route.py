from flask import jsonify, request
import requests

def login():
    username = request.headers.get('username', None)
    password = request.headers.get('password', None)
    print(username)

    error_details = {}
    error_status = False

    if username is None:
        error_details['username_empty'] = True
        error_status = True
    if password is None:
        error_details['password_empty'] = True
        error_status = True

    if error_status:
        response = {
            "status": "login_failed",
            "errors": error_details
        }
        return jsonify(response), 400

    url = "http://127.0.0.1:5000/login"
    request_parameter = {
        "username": username,
        "password": password
    }

    auth_service_request = requests.get(url, headers=request_parameter)
    print("login route, do request to auth service")
    if auth_service_request.status_code == 200:
        response_data = auth_service_request.json()
        print(response_data)

        response = {
            "status": "login_successful",
            "uid": response_data['uid'],
            "new_access_token": response_data['new_access_token'],
            "new_refresh_token": response_data['new_refresh_token']
        }
        return jsonify(response), auth_service_request.status_code
    else:
        response = {
            "status": "login_failed"
        }
        return jsonify(response), auth_service_request.status_code
