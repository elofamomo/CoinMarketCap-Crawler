import spyql
import json


def switch_case_response(status_code, data):
    if status_code == 200:
        return accept(data)
    elif status_code == 400:
        return bad_request(data)
    elif status_code == 401:
        return unauthorized(data)
    elif status_code == 403:
        return forbidden(data)
    elif status_code == 404:
        return not_found(data)
    elif status_code == 429:
        return too_many_request(data)
    elif status_code == 500:
        return internal_server_error(data)
    else:
        return unknown_error(status_code, data)


def accept(data):
    print("Request done")
    print("Writing to csv file... ")


def bad_request(data):
    print(f"Error request: {data['status']['error_message']}")


def unauthorized(data):
    print(f"Error request: {data['status']['error_message']}")


def forbidden(data):
    print(f"Error request: {data['status']['error_message']}")


def not_found(data):
    print(f"Error request: {data['error']}")


def too_many_request(data):
    print(f"Error request: {data['status']['error_message']}")


def internal_server_error(data):
    print(f"Error request: {data['status']['error_message']}")


def unknown_error(status_code, data):
    print(f"Unknown request error, \n status code : {status_code} \n , data: {data}")
