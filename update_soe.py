"""
------------------------------------------------------------------------------
Name:        update_soe.py
Purpose:     Update Server Object Extension from command line
Author:      Josh Werts (@jwerts) (joshwerts@gmail.com)
Created:     4/12/15
License      MIT
-------------------------------------------------------------------------------
"""﻿

from __future__ import print_function

# 3rd-party library: requests
# http://docs.python-requests.org/en/latest/
# pip install requests
import requests

PROTOCOL = "http://"
HOST = "localhost"
USER = "siteadmin"
PASSWORD = "yourpassword"

# note that services are suffixed by type when passed to admin REST API
SERVICES = [r"service_folder\service_name.MapServer"]

# path to rebuilt SOE file
SOE_FILE = r"C:\path_to_your_project\bin\Debug\yourSOE.soe"

class AGSRestError(Exception): pass
class ServerError(Exception): pass

def _validate_response(response):
    if not response.ok:
        raise ServerError("Server Error: {}".format(response.text))

    try:
        response_json = response.json()
        if "error" in response_json:
            raise AGSRestError(response_json["error"])
        if "status" in response_json and response_json["status"] != "success":
            error = response_json["status"]
            if "messages" in response_json:
                for message in response_json["messages"]:
                    error += "\n" + message
            raise AGSRestError(error)

    except ValueError:
        print(response.text)
        raise ServerError("Server returned HTML: {}".format(response.text))


def _get_token():
    token_url = "{protocol}{host}/arcgis/tokens/".format(
        protocol=PROTOCOL, host=HOST)

    data = { "f": "json",
             "username": USER,
             "password": PASSWORD,
             "client": "requestip",
             "expiration": 5 }
    response = requests.post(token_url, data)
    _validate_response(response)
    token = response.json()['token']
    return token


def _upload_soe_file(token):
    upload_url = "{protocol}{host}/arcgis/admin/uploads/upload?f=json".format(
        protocol=PROTOCOL, host=HOST)

    with open(SOE_FILE, 'rb') as soe_file:
        files = {'itemFile': soe_file}
        data = {
            "token": token
        }
        response = requests.post(upload_url, data, files=files)

    _validate_response(response)
    response_json = response.json()
    item_id = response_json['item']['itemID']

    return item_id


def _update_soe(item_id, token):
    update_url = "{protocol}{host}/arcgis/admin/services/types/extensions/update".format(
        protocol=PROTOCOL, host=HOST)

    data = {
        "f": "json",
        "token": token,
        "id": item_id
    }
    response = requests.post(update_url, data)
    _validate_response(response)


def _start_services(token):
    start_services_url = "{protocol}{host}/arcgis/admin/services/{service}/start"

    for service in SERVICES:
        url = start_services_url.format(protocol=PROTOCOL,
                                        host=HOST,
                                        service=service)
        print("Starting {}".format(service))

        data = {
            "f": "json",
            "token": token,
        }
        response = requests.post(url, data)
        _validate_response(response)
        print("Started!")


if __name__ == "__main__":
    print("Retrieving token...")
    token = _get_token()
    print("Retrieved: {}".format(token))

    print("Uploading SOE...")
    item_id = _upload_soe_file(token)
    print("Uploaded: {}".format(item_id))

    print("Updating SOE...")
    _update_soe(item_id, token)
    print("Updated!")

    print("Starting services...")
    _start_services(token)
