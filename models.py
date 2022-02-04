import sqlite3
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
        self._create_table(self.connection, self.table_name, columns=[self.key, 'trademark', 'producer'])
        self.id = next(autoincrement)
        self.trademark = trademark
        self.producer = producer

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __del__(self):
        deletion_command = f"DELETE FROM {self.table_name} WHERE {self.key}=?;"
        self.connection.execute(deletion_command, [self.id])
        self.connection.commit()

    @staticmethod
    def _create_table(connection, table_name, columns):
        create_table_command = f"""CREATE TABLE IF NOT EXISTS {table_name} 
            ({columns[0]} int PRIMARY KEY, {columns[1]} varchar(255), {columns[2]} varchar(255));"""
        connection.execute(create_table_command)
