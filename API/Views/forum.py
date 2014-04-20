from API.forum_tools import forums
from API.post_tools import posts
from API.Views.handlers.requesthand import GET_parameters, get_opt, get_relate
from API.thread_tools import threads

__author__ = 'tan'

from API.Views.handlers.handlers import return_response, test_require, return_error
import json
from django.http import HttpResponse

def create(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["name", "short_name", "user"]
        try:
            test_require(data=request_info, required=required_info)
            forum = forums.add_forum(name=request_info["name"], short_name=request_info["short_name"],
                                      user=request_info["user"])
        except Exception as e:
            print("name = " + request_info["name"])
            print("short_name = " + request_info["short_name"])
            print("user = " + request_info["user"])
            print(e.message)
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["forum"]
        relate = get_relate(request_info)
        try:
            test_require(data=request_info, required=required_info)
            forum = forums.details(short_name=request_info["forum"], related=relate)
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def list_threads(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["forum"]
        relate = get_relate(request_info)
        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since"])
        try:
            test_require(data=request_info, required=required_info)
            threads_array = threads.threads_list(table_="forum", parametr=request_info["forum"],
                                             related=relate, params=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(threads_array)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["forum"]
        relate = get_relate(request_info)
        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since"])
        try:
            test_require(data=request_info, required=required_info)
            posts_array = posts.posts_list(table_="forum", parametr=request_info["forum"],
                                       related=relate, params=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_array)
    else:
        return HttpResponse(status=400)


def list_users(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["forum"]
        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since_id"])
        try:
            test_require(data=request_info, required=required_info)
            users_array = forums.list_users(request_info["forum"], opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(users_array)
    else:
        return HttpResponse(status=400)