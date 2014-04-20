import json

from django.http import HttpResponse

from API.db_tools.select import selectQuery
from API.db_tools.update import ins_upd_delQuery
from API.db_tools.verifyer import verify
from API.user_tools import users
import API.post_tools.posts as posts
from API.Views.handlers.handlers import test_require, return_error, return_response
from API.Views.handlers.requesthand import get_opt


__author__ = 'taniy'


def add_follows(email1, email2):
    verify(table_name="Users", param="email", val=email1)
    verify(table_name="Users", param="email", val=email2)
    if email1 == email2:
        raise Exception("User with email=" + email1 + " can't follow himself")
    follows = selectQuery('SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))
    if len(follows) == 0:
        ins_upd_delQuery('INSERT INTO Followers (follower, followee) VALUES (%s, %s)', (email1, email2, ))
    user = users.details(email1)
    return user


def remove_follows(email1, email2):
    follows = selectQuery('SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))
    if len(follows) != 0:
        ins_upd_delQuery('DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))
    else:
        raise Exception("No such following")
    return users.details(email1)


def followers_list(email, type, params):
    verify(table_name="Users", param="email", val=email)
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    query = "SELECT "+type+" FROM Followers, Users WHERE Users.email = Followers."+type+\
            " AND "+where+" = %s "
    if "since_id" in params:
        query += " AND Users.id >= "+str(params["since_id"])
    if "order" in params:
        query += " ORDER BY Users.name "+params["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in params:
        query += " LIMIT "+str(params["limit"])
    followers_ids_tuple = selectQuery(query=query, params=(email, ))
    followers_array = []
    for id in followers_ids_tuple:
        id = id[0]
        followers_array.append(users.details(email=id))
    return followers_array


def create(request):
    if request.method == "POST":
        request_info = json.loads(request.body)
        required_info = ["user", "forum", "thread", "message", "date"]
        optional_info = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        opt = get_opt(request_info=request_info, possible_values=optional_info)
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