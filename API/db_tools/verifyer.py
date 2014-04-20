from API.db_tools.select import selectQuery

__author__ = 'taniy'


def verify(table_name, param, val):
    if not len(selectQuery('SELECT id FROM ' + table_name + ' WHERE ' + param + ' = %s', (val, ))):
        raise Exception("Impossible to do something with element")
    return