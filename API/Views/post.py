from API.post_tools import posts
from API.Views.handlers.requesthand import GET_parameters, get_opt, get_relate

__author__ = 'tan'

import json
from django.http import HttpResponse
from API.Views.handlers.handlers import test_require, return_response, return_error


def create(request):
    if request.method == "POST":

        request_info = json.loads(request.body)
        required_info = ["user", "forum", "thread", "message", "date"]
        opt_info = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        opt = get_opt(request_info=request_info, possible_values=opt_info)
        try:
            test_require(data=request_info, required=required_info)
            newpost = posts.create(date=request_info["date"], thread=request_info["thread"],
                                message=request_info["message"], user=request_info["user"],
                                forum=request_info["forum"], opt=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(newpost)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["post"]
        relate = get_relate(request_info)
        try:
            test_require(data=request_info, required=required_info)
            post = posts.details(request_info["post"], related=relate)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def post_list(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        param = None
        try:
            param = request_info["forum"]
            table_name = "forum"
        except KeyError:
            try:
                param = request_info["thread"]
                table_name = "thread"
            except KeyError:
                return return_error("No thread or forum parameters in request")

        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since"])
        try:
            post_array = posts.posts_list(table_=table_name, parametr=param, related=[], params=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(post_array)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["post"]
        try:
            test_require(data=request_info, required=required_info)
            delete_post = posts.remove_restore(post_id=request_info["post"], status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(delete_post)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["post"]
        try:
            test_require(data=request_info, required=required_info)
            post = posts.remove_restore(post_id=request_info["post"], status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["post", "message"]
        try:
            test_require(data=request_info, required=required_info)
            modify_post = posts.update(id=request_info["post"], message=request_info["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(modify_post)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["post", "vote"]
        try:
            test_require(data=request_info, required=required_info)
            post = posts.vote(id=request_info["post"], vote=request_info["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)