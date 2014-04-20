import MySQLdb

from API.db_tools.dbconnect import Connector


__author__ = 'taniy'


def selectQuery(query, params):
    try:
        connect = Connector()
        connect = connect.connect()
        with connect:
            cursor = connect.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
        connect.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("select Error")
    return result