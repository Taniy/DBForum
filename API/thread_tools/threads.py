from API.db_tools.select import selectQuery
from API.db_tools.update import ins_upd_delQuery
from API.db_tools.verifyer import verify
from API.forum_tools import forums
from API.user_tools import users

__author__ = 'taniy'


def add_threads(forum, title, isClosed, user, date, message, slug, optional):
    verify(table_name="Users", param="email", val=user)
    verify(table_name="Forums", param="short_name", val=forum)
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    thread = selectQuery(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(thread) == 0:
        ins_upd_delQuery(
            'INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (forum, title, isClosed, user, date, message, slug, isDeleted, )
        )
        thread = selectQuery(
            'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    response = threads_info(thread)
    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]
    return response


def details(id, related):
    thread = selectQuery(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (id, )
    )
    if len(thread) == 0:
        raise Exception('No thread exists with id=' + str(id))
    thread = threads_info(thread)

    if "user" in related:
        thread["user"] = users.details(thread["user"])
    if "forum" in related:
        thread["forum"] = forums.details(short_name=thread["forum"], related=[])
    return thread


def threads_info(thread):
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }
    return response


def vote(id, vote):
    verify(table_name="Threads", param="id", val=id)
    if vote == -1:
        ins_upd_delQuery("UPDATE Threads SET dislikes=dislikes+1, points=points-1 WHERE id = %s", (id, ))
    else:
        ins_upd_delQuery("UPDATE Threads SET likes=likes+1, points=points+1  WHERE id = %s", (id, ))
    return details(id=id, related=[])


def open_close_threads(id, isClosed):
    verify(table_name="Threads", param="id", val=id)
    ins_upd_delQuery("UPDATE Threads SET isClosed = %s WHERE id = %s", (isClosed, id, ))
    response = {
        "thread": id
    }
    return response


def update_threads(id, slug, message):
    verify(table_name="Threads", param="id", val=id)
    ins_upd_delQuery('UPDATE Threads SET slug = %s, message = %s WHERE id = %s',(slug, message, id, ))
    return details(id=id, related=[])


def threads_list(table_, parametr, related, params):
    if table_ == "forum":
        verify(table_name="Forums", param="short_name", val=parametr)
    if table_ == "user":
        verify(table_name="Users", param="email", val=parametr)
    query = "SELECT id FROM Threads WHERE " + table_ + " = %s "
    parameters = [parametr]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    thread_ids_tuple = selectQuery(query=query, params=parameters)
    thread_array = []
    for id in thread_ids_tuple:
        id = id[0]
        thread_array.append(details(id=id, related=related))
    return thread_array


def remove_restore(thread_id, status):
    verify(table_name="Threads", param="id", val=thread_id)
    ins_upd_delQuery("UPDATE Threads SET isDeleted = %s WHERE id = %s", (status, thread_id, ))
    response = {
        "thread": thread_id
    }
    return response