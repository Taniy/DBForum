import MySQLdb

__author__ = 'taniy'


class Connector:

    def __init__(self):
        pass
    host = "localhost"
    u = "root"
    p = "123"
    db = "DBForums"

    def connect(self):
        return MySQLdb.connect(self.host, self.u, self.p, self.db, init_command='set names UTF8')


