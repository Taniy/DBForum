from API.post_tools import posts
from API.Views.handlers.requesthand import GET_parameters, get_opt, get_relate
from API.thread_tools import threads, subscriptions

__author__ = 'tan'

from API.Views.handlers.handlers import return_response, test_require, return_error
import json
from django.http import HttpResponse


def close(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread"]
        try:
            test_require(data=request_info, required=required_info)
            thread = threads.open_close_threads(id=request_info["thread"], isClosed=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def create(request):
    if request.method == "POST":

        request_info = json.loads(request.body)
        required_info = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        opt = get_opt(request_info=request_info, possible_values=["isDeleted"])
        try:
            test_require(data=request_info, required=required_info)
            new_thread = threads.add_threads(forum=request_info["forum"], title=request_info["title"], isClosed=request_info["isClosed"],
                                     user=request_info["user"], date=request_info["date"], message=request_info["message"],
                                     slug=request_info["slug"], optional=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(new_thread)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["thread"]
        relate = get_relate(request_info)
        try:
            test_require(data=request_info, required=required_info)
            thread = threads.details(id=request_info["thread"], related=relate)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def threads_list(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        param = None
        try:
            param = request_info["forum"]
            table_name = "forum"
        except KeyError:
            try:
                param = request_info["user"]
                table_name = "user"
            except KeyError:
                return return_error("No user or forum parameters setted")
        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since"])
        try:
            threads_array = threads.threads_list(table_=table_name, parametr=param, related=[], params=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(threads_array)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["thread"]
        table_name = "thread"
        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since"])
        try:
            test_require(data=request_info, required=required_info)
            post_array = posts.posts_list(table_=table_name, parametr=request_info["thread"], related=[], params=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(post_array)
    else:
        return HttpResponse(status=400)


def open(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread"]
        try:
            test_require(data=request_info, required=required_info)
            thread = threads.open_close_threads(id=request_info["thread"], isClosed=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread"]
        try:
            test_require(data=request_info, required=required_info)
            delete_thread = threads.remove_restore(thread_id=request_info["thread"], status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(delete_thread)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread"]
        try:
            test_require(data=request_info, required=required_info)
            thread = threads.remove_restore(thread_id=request_info["thread"], status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def subscribe(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread", "user"]
        try:
            test_require(data=request_info, required=required_info)
            subscription = subscriptions.add_subscriptions(email=request_info["user"], thread_id=request_info["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def unsubscribe(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread", "user"]
        try:
            test_require(data=request_info, required=required_info)
            subscription = subscriptions.remove_subscriptions(email=request_info["user"], thread_id=request_info["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread", "slug", "message"]
        try:
            test_require(data=request_info, required=required_info)
            modify_thread = threads.update_threads(id=request_info["thread"], slug=request_info["slug"], message=request_info["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(modify_thread)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["thread", "vote"]
        try:
            test_require(data=request_info, required=required_info)
            thread = threads.vote(id=request_info["thread"], vote=request_info["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)

