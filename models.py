import sqlite3
from typing import List

import settings
from db.fields import (
    Field,
)


def generate_ints():
    i = 1
    while True:
        yield i
        i += 1


autoincrement = generate_ints()


class SoftDrink(object):
    key = 'pk'
    table_name = f'{__qualname__.lower()}s_table'
    trademark = Field(max_length=8)
    producer = Field(max_length=8)

    def __init__(self, trademark: str, producer: str, ):
        self.connection = sqlite3.connect(settings.DATABASES["DEFAULT"])
        self._create_table(self.connection, extra=[self.table_name, self.key, *self._get_descriptor_columns()])
        self.id = next(autoincrement)
        self.trademark = trademark
        self.producer = producer

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
