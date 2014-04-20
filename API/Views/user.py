from API.post_tools import posts
from API.user_tools import users, followers
from API.Views.handlers.requesthand import GET_parameters, get_opt

__author__ = 'tan'


from API.Views.handlers.handlers import return_response, test_require, return_error
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["email", "username", "name", "about"]
        opt = get_opt(request_info=request_info, possible_values=["isAnonymous"])
        try:
            test_require(data=request_info, required=required_info)
            new_user = users.add_users(email=request_info["email"], username=request_info["username"],
                               about=request_info["about"], name=request_info["name"], optional=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(new_user)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["user"]
        try:
            test_require(data=request_info, required=required_info)
            user_details = users.details(email=request_info["user"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user_details)
    else:
        return HttpResponse(status=400)


def follow(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["follower", "followee"]
        try:
            test_require(data=request_info, required=required_info)
            following_array = followers.add_follows(email1=request_info["follower"], email2=request_info["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following_array)
    else:
        return HttpResponse(status=400)


def list_followers(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["user"]
        followers_opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since_id"])
        try:
            test_require(data=request_info, required=required_info)
            follower_array = followers.followers_list(email=request_info["user"], type="follower", params=followers_opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(follower_array)
    else:
        return HttpResponse(status=400)


def list_following(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["user"]
        followers_opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since_id"])
        try:
            test_require(data=request_info, required=required_info)
            followings_array = followers.followers_list(email=request_info["user"], type="followee", params=followers_opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(followings_array)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_info = GET_parameters(request)
        required_info = ["user"]
        opt = get_opt(request_info=request_info, possible_values=["limit", "order", "since"])
        try:
            test_require(data=request_info, required=required_info)
            posts_array = posts.posts_list(table_="user", parametr=request_info["user"], related=[], params=opt)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_array)
    else:
        return HttpResponse(status=400)


def unfollow(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["follower", "followee"]
        try:
            test_require(data=request_info, required=required_info)
            following_array = followers.remove_follows(email1=request_info["follower"], email2=request_info["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following_array)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["user", "name", "about"]
        try:
            test_require(data=request_info, required=required_info)
            modify_user = users.update_users(email=request_info["user"], name=request_info["name"], about=request_info["about"])
        except Exception as e:
            return return_error(e.message)
        return return_response(modify_user)
    else:
        return HttpResponse(status=400)