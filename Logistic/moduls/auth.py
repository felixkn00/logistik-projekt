from flask import request, jsonify
import requests


def auth(uid, access_token, refresh_token=None):
    print("run auth function")

    error_details = {}
    error_status = False

    if uid is None or uid == "":
        error_details['uid_empty'] = True
        error_status = True
    if access_token is None or access_token == "":
        error_details['access_token_empty'] = True
        error_status = True

    if error_status:
        response = {
            "status": "access_token_auth_failed",
            "errors": error_details
        }
        print(f"auth function response: {response}")
        return response

    url = "http://127.0.0.1:5000/auth"
    request_parameter = {
        "uid": uid,
        "accesstoken": access_token
    }

    try:
        auth_service_request = requests.post(url, headers=request_parameter)
        auth_service_request.raise_for_status()

        response_data = auth_service_request.json()

        if response_data.get('status') == 'access_token_auth_successful':
            response = {
                "status": "access_token_auth_successful",
                "new_access_token": response_data.get('new_access_token'),
            }
            print(f"auth function success response: {response}")
            return response

        elif response_data.get('status') == 'access_token_auth_failed':
            if refresh_token:
                print("access token invalid")
                refresh_url = "http://127.0.0.1:5000/auth/refresh"
                refresh_request_params = {
                    "uid": uid,
                    "refreshtoken": refresh_token
                }

                try:
                    refresh_response = requests.post(refresh_url, headers=refresh_request_params)
                    refresh_response.raise_for_status()
                    refresh_data = refresh_response.json()

                    if refresh_data.get('status') == 'refresh_successful':
                        response = {
                            "status": "token_refresh_successful",
                            "new_access_token": refresh_data.get('new_access_token'),
                        }
                        print(f"refresh access_token success response: {response}")
                        return response
                    else:
                        response = {
                            "status": "refresh_token_auth_failed",
                            "errors": {"refresh_token_invalid": True}
                        }
                        print(f"refresh token failed response: {response}")
                        return response

                except requests.exceptions.RequestException as refresh_error:
                    print(f"request with refresh token failed: {refresh_error}")
                    return {
                        "status": "refresh_token_auth_failed",
                        "errors": {"refresh_service_error": str(refresh_error)}
                    }
            else:
                print("access token invalid")
                return {
                    "status": "access_token_auth_failed",
                    "errors": {"no_refresh_token": True}
                }

        else:
            response = {
                "status": "access_token_auth_failed",
                "errors": {"unexpected_status": response_data.get('status')}
            }
            print(f"auth function unexpected response: {response}")
            return response

    except requests.exceptions.RequestException as e:
        print(f"request auth service failed: {e}")
        return {
            "status": "access_token_auth_failed",
            "errors": {"auth_service_error": str(e)}
        }