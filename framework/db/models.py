from beverages_app.settings import DB_CONNECTION
from framework.tools.dispatcher import pre_init
from typing import List
from framework.db.fields import (
    Field,
)


def generate_ints():
    i = 1
    while True:
        yield i
        i += 1


autoincrement = generate_ints()


class BaseModel(object):
    key = 'pk'
    connection = DB_CONNECTION

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        callbacks = pre_init.check_signals_registry(instance.__class__.__name__)
        if callbacks:
            for callback in callbacks:
                callback()
        return instance

    def __init__(self):
        self.table_name = f'{self.__class__.__name__.lower()}s_table'
        self.id = next(autoincrement)
        self._create_table(
            self.connection, extra=[
                self.table_name,
                self.key,
                *self._get_descriptor_columns()
            ]
        )

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __del__(self):
        deletion_command = f"DELETE FROM {self.table_name} WHERE {self.key}=?;"
        self.connection.execute(deletion_command, [self.id])
        self.connection.commit()

    def _get_descriptor_columns(self) -> List[str]:
        column_names = []
        attrs = vars(self.__class__)
        for k, v in attrs.items():
            if isinstance(v, Field):
                column_names.append(k)
        return column_names

    @staticmethod
    def _create_table(connection, extra):
        create_table_cmd = "CREATE TABLE IF NOT EXISTS {0} ({1} int PRIMARY KEY, {2} varchar(255), {3} varchar(255));"
        connection.execute(create_table_cmd.format(*extra))
