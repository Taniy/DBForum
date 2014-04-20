from API.db_tools.select import selectQuery
from API.db_tools.update import ins_upd_delQuery
from API.db_tools.verifyer import verify

__author__ = 'taniy'


def add_users(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        user = select_user('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
        if len(user) == 0:
            ins_upd_delQuery(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = select_user('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
    except Exception as e:
        raise Exception(e.message)
    return users_info(user)


def update_users(email, about, name):
    verify(table_name="Users", param="email", val=email)
    ins_upd_delQuery('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s', (email, about, name, email, ))
    return details(email)


def followers(email, type):
    where = "followee"
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    f_list = selectQuery(
        "SELECT " + type + " FROM Followers, Users WHERE Users.email = Followers." + type +
        " AND " + where + " = %s ", (email, )
    )
    return tuple_list(f_list)


def details(email):
    user = users_query(email)
    if user is None:
        raise Exception("No user with email " + email)
    user["followers"] = followers(email, "follower")
    user["following"] = followers(email, "followee")
    user["subscriptions"] = users_subscriptions(email)
    return user


def users_subscriptions(email):
    subscriptions_array = []
    subscriptions = selectQuery('select thread FROM Subscriptions WHERE user = %s', (email, ))
    for el in subscriptions:
        subscriptions_array.append(el[0])
    return subscriptions_array


def users_query(email):
    user = select_user('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
    if len(user) == 0:
        return None
    return users_info(user)


def users_info(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response


def select_user(query, params):
    return selectQuery(query, params)


def tuple_list(list):
    new_list = []
    for el in list:
        new_list.append(el[0])
    return new_list