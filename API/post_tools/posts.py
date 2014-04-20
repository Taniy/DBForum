from API.db_tools.dbconnect import Connector
from API.db_tools.select import selectQuery
from API.db_tools.update import ins_upd_delQuery
from API.db_tools.verifyer import verify
from API.forum_tools import forums
from API.thread_tools import threads
from API.user_tools import users

__author__ = 'taniy'


def create(date, thread, message, user, forum, opt):
    verify(table_name="Threads", param="id", val=thread)
    verify(table_name="Forums", param="short_name", val=forum)
    verify(table_name="Users", param="email", val=user)
    if len(selectQuery("SELECT Threads.id FROM Threads,Forums WHERE Threads.forum = Forums.short_name "
                                "AND Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("no thread with id = " + thread + " in forum " + forum)
    if "parent" in opt:
        if len(selectQuery("SELECT Posts.id FROM Posts, Threads WHERE Threads.id = Posts.thread "
                             "AND Posts.id = %s AND Threads.id = %s", (opt["parent"], thread, ))) == 0:
            raise Exception("No post with id = " + opt["parent"])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]
    for param in opt:
        query += ", "+param
        values += ", %s"
        parameters.append(opt[param])
    query += ") VALUES " + values + ")"
    update_thread_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"
    con = Connector()
    con = con.connect()
    con.autocommit(False)
    with con:
        cursor = con.cursor()
        try:
            con.begin()
            cursor.execute(update_thread_posts, (thread, ))
            cursor.execute(query, parameters)
            con.commit()
        except Exception as e:
            con.rollback()
            raise Exception("Database error: " + e.message)
        #DatabaseConnection.connection.commit()
        post_id = cursor.lastrowid
        cursor.close()
    con.close()
    post = posts_query(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def details(id, related):
    post = posts_query(id)
    if post is None:
        raise Exception("no post with id = "+id)
    if "user" in related:
        post["user"] = users.details(post["user"])
    if "forum" in related:
        post["forum"] = forums.details(short_name=post["forum"], related=[])
    if "thread" in related:
        post["thread"] = threads.details(id=post["thread"], related=[])
    return post


def posts_list(table_, parametr, related, params):
    if table_ == "forum":
        verify(table_name="Forums", param="short_name", val=parametr)
    if table_ == "thread":
        verify(table_name="Threads", param="id", val=parametr)
    if table_ == "user":
        verify(table_name="Users", param="email", val=parametr)
    query = "SELECT id FROM Posts WHERE " + table_ + " = %s "
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
    post_ids = selectQuery(query=query, params=parameters)
    post_list = []
    for id in post_ids:
        id = id[0]
        post_list.append(details(id=id, related=related))
    return post_list


def remove_restore(post_id, status):
    verify(table_name="Posts", param="id", val=post_id)
    ins_upd_delQuery("UPDATE Posts SET isDeleted = %s WHERE Posts.id = %s", (status, post_id, ))
    return {
        "post": post_id
    }


def update(id, message):
    verify(table_name="Posts", param="id", val=id)
    ins_upd_delQuery('UPDATE Posts SET message = %s WHERE id = %s', (message, id, ))
    return details(id=id, related=[])


def vote(id, vote):
    verify(table_name="Posts", param="id", val=id)
    if vote == -1:
        ins_upd_delQuery("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        ins_upd_delQuery("UPDATE Posts SET likes=likes+1, points=points+1  where id = %s", (id, ))
    return details(id=id, related=[])


def select_posts(query, params):
    return selectQuery(query, params)


def posts_query(id):
    post = select_posts('select date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM Posts WHERE id = %s', (id, ))
    if len(post) == 0:
        return None
    return posts_info(post)


def posts_info(post):
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],
    }
    return post_response
