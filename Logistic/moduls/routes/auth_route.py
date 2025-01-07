import requests
from flask import jsonify, request

def auth():
    uid = request.headers.get('uid')
    access_token = request.headers.get('accesstoken')
    refresh_token = request.headers.get('refreshtoken')

    print("auth guard")
    print(refresh_token)

    url = "http://127.0.0.1:5000/auth"
    request_parameter = {
        "uid": uid,
        "accesstoken": access_token
    }

    try:
        auth_service_request = requests.post(url, headers=request_parameter)
        res = auth_service_request.json()

        if auth_service_request.status_code == 200:
            response = {
                "status": "access_token_auth_successful",
                "new_access_token": res["new_access_token"]
            }
            return jsonify(response), 200
        else:
            if auth_service_request.status_code == 401 and refresh_token:
                refresh_url = "http://127.0.0.1:5000/refresh"
                refresh_request_parameters = {
                    "uid": uid,
                    "refreshtoken": refresh_token
                }

                refresh_request = requests.post(refresh_url, headers=refresh_request_parameters)
                refresh_res = refresh_request.json()

                if refresh_request.status_code == 200:
                    new_access_token = refresh_res["new_access_token"]

                    retry_request_parameter = {
                        "uid": uid,
                        "access_token": new_access_token
                    }

                    retry_auth_request = requests.post(url, headers=retry_request_parameter)
                    retry_res = retry_auth_request.json()

                    if retry_auth_request.status_code == 200:
                        response = {
                            "status": "access_token_auth_successful",
                            "new_token": retry_res["new_token"]
                        }
                        return jsonify(response), 200
                    else:
                        response = {
                            "status": retry_res["status"],
                            "errors": retry_res['errors']
                        }
                        return jsonify(response), 401
                else:
                    response = {
                        "status": refresh_res["status"],
                        "errors": refresh_res["errors"]
                    }
                    return jsonify(response), 401
            else:
                response = {
                    "status": res["status"],
                    "errors": res['errors']
                }
                return jsonify(response), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
