from API.db_tools.select import selectQuery
from API.db_tools.update import ins_upd_delQuery
from API.db_tools.verifyer import verify
from API.user_tools import users

def add_forum(name, short_name, user):
    verify(table_name="Users", param="email", val=user)
    forum = selectQuery('SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    if len(forum) == 0:
        ins_upd_delQuery('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)', (name, short_name, user, ))
        forum = selectQuery('SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    return forums_info(forum)


def forums_info(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def details(short_name, related):
    forum = selectQuery('SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    if len(forum) == 0:
        raise ("No forum with exists short_name=" + short_name)
    forum = forums_info(forum)
    if "user" in related:
        forum["user"] = users.details(forum["user"])
    return forum


def list_users(short_name, opt):
    verify(table_name="Forums", param="short_name", val=short_name)

    query = "SELECT distinct email FROM Users, Posts, Forums WHERE Posts.user = Users.email " \
            " and Forums.short_name = Posts.forum and Posts.forum = %s "
    if "since_id" in opt:
        query += " AND Users.id >= " + str(opt["since_id"])
    if "order" in opt:
        query += " ORDER BY Users.id " + opt["order"]
    if "limit" in opt:
        query += " LIMIT " + str(opt["limit"])
    users_tuple = selectQuery(query, (short_name, ))
    user_array = []
    for user in users_tuple:
        user = user[0]
        user_array.append(users.details(user))
    return user_array
