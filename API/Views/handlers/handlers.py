__author__ = 'tan'

import json

from django.http import HttpResponse

def return_response(object):
    response_info = {"code": 0, "response": object}
    return HttpResponse(json.dumps(response_info), content_type='application/json')


def return_error(message):
    response_info = {"code": 1, "response": message}
    return HttpResponse(json.dumps(response_info), content_type='application/json')


def test_require(data, required):
    for el in required:
        if el not in data:
            raise Exception("required element " + el + " not in parameters")
        if data[el] is not None:
            try:
                data[el] = data[el].encode('utf-8')
            except Exception:
                continue

    return


