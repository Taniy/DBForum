from API.db_tools.select import selectQuery
from API.db_tools.update import ins_upd_delQuery
from API.db_tools.verifyer import verify

__author__ = 'taniy'


def add_subscriptions(email, thread_id):
    verify(table_name="Threads", param="id", val=thread_id)
    verify(table_name="Users", param="email", val=email)
    subscription = selectQuery(
        'select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        ins_upd_delQuery('INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email, ))
        subscription = selectQuery(
            'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
        )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def remove_subscriptions(email, thread_id):
    verify(table_name="Threads", param="id", val=thread_id)
    verify(table_name="Users", param="email", val=email)
    subscriptions = selectQuery(
        'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscriptions) == 0:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    ins_upd_delQuery('DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, ))
    response = {
        "thread": subscriptions[0][0],
        "user": subscriptions[0][1]
    }
    return response