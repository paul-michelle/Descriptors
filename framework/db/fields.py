import sqlite3

VARCHAR_LENGTH = 255


class BaseFieldDescriptor(object):
    def __set_name__(self, owner, name):
        raise NotImplementedError

    def __get__(self, instance, owner):
        raise NotImplementedError

    def __set__(self, instance, value):
        raise NotImplementedError

    def _validate(self, *args, **kwargs):
        raise NotImplementedError


class Field(BaseFieldDescriptor):

    def __init__(self, max_length: int = VARCHAR_LENGTH):
        self._max_length = max_length

    def __set_name__(self, owner, name):
        self._table_name = f'{owner.__name__.lower()}s_table'
        self._retrieve = f'SELECT {name} FROM {self._table_name} WHERE {owner.key}=?;'
        self._update = f"""
            INSERT INTO {self._table_name}({owner.key}, {name}) VALUES(?, ?) 
            ON CONFLICT({owner.key}) DO UPDATE SET {name}=?;
            """

    def __get__(self, instance, owner):
        connection = self._get_connection(instance)
        try:
            exe_results = connection.execute(self._retrieve, [instance.id]).fetchone()
        except sqlite3.OperationalError as e:
            raise RuntimeError(f'ERROR! {e}') from e
        return exe_results[0]

    def __set__(self, instance, value):
        self._validate(value=value)
        connection = self._get_connection(instance)
        connection.execute(self._update, [instance.id, value, value])
        connection.commit()

    def _validate(self, *args, **kwargs):
        if not isinstance(kwargs['value'], str):
            raise ValueError('The value must be a string')
        if len(kwargs['value']) > self._max_length:
            raise ValueError(f'The value may not exceed {self._max_length} chars')

    @staticmethod
    def _get_connection(instance):
        try:
            connection = instance['connection'] or instance['conn']
        except KeyError:
            raise RuntimeError('Failed to determine database connection')
        return connection
