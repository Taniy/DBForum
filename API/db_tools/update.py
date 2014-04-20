import MySQLdb

from API.db_tools.dbconnect import Connector


__author__ = 'taniy'


def ins_upd_delQuery(query, params):
    try:
        connect = Connector()
        connect = connect.connect()
        with connect:
            cursor = connect.cursor()
            connect.begin()
            cursor.execute(query, params)
            connect.commit()
            cursor.close()
            id = cursor.lastrowid
        connect.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Update error")
    return id