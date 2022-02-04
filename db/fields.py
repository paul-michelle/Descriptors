import sqlite3


def get_connection(instance):
    try:
        connection = instance['connection'] or instance['conn']
    except KeyError:
        raise RuntimeError('Failed to determine database connection')
    return connection


def auto_increase():
    i = 1
    while True:
        yield i
        i += 1


class Field(object):

    def __set_name__(self, owner, name):
        self._retrieve = f'SELECT {name} FROM {owner.table_name} WHERE {owner.key}=?'
        self._update = f"""
            INSERT INTO {owner.table_name}({owner.key}, {name}) VALUES(?, ?) 
            ON CONFLICT({owner.key}) DO UPDATE SET {name}=?
            """

        self._remove = f'DELETE FROM {owner.table_name} WHERE {owner.key}=?'

    def __get__(self, instance, owner):
        connection = get_connection(instance)
        try:
            exe_results = connection.execute(self._retrieve, [instance.id]).fetchone()
        except sqlite3.OperationalError as e:
            raise RuntimeError(f'ERROR! {e}') from e
        return exe_results[0]

    def __set__(self, instance, value):
        connection = get_connection(instance)
        connection.execute(self._update, [instance.id, value, value])
        connection.commit()

    def __delete__(self, instance):
        connection = get_connection(instance)
        connection.execute(self._remove, [instance.id])
        connection.commit()
