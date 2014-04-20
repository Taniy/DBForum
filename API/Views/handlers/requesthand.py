import json

from django.http import HttpResponse

from API.post_tools import posts as posts
from API.Views.handlers.handlers import test_require, return_error, return_response


__author__ = 'tan'


def create(request):
    if request.method == "POST":

        request_info = json.loads(request.body)
        required_info = ["user", "forum", "thread", "message", "date"]
        opt_info = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        opt = get_opt(request_info=request_info, possible_values=opt_info)
        try:
            test_require(data=request_info, required=required_info)
            post = posts.create(date=request_info["date"], thread=request_info["thread"],
                                message=request_info["message"], user=request_info["user"],
                                forum=request_info["forum"], opt=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def GET_parameters(request_info):
    data = {}
    for el in request_info.GET:
        data[el] = request_info.GET.get(el)
    return data


def get_opt(request_info, possible_values):
    opt = {}
    for value in possible_values:
        try:
            opt[value] = request_info[value]
        except KeyError:
            continue
    return opt


def get_relate(request_info):
    try:
        related = request_info["related"]
    except KeyError:
        related = []
    return related