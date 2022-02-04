import sqlite3
from db.fields import (
    Field,
    auto_increase
)

autoincrement = auto_increase()


def create_table(connection, table_name, columns):
    create_table_command = f"""CREATE TABLE IF NOT EXISTS {table_name} 
        ({columns[0]} int PRIMARY KEY, {columns[1]} varchar(255), {columns[2]} varchar(255));"""
    connection.execute(create_table_command)


class SoftDrink(object):
    connection = sqlite3.connect('beverages')
    table_name = 'soft_drinks'
    key = 'pk'
    create_table(connection, table_name, columns=['pk', 'trademark', 'producer'])

    trademark = Field()
    producer = Field()

    def __init__(self, trademark: str, producer: str, ):
        self.id = next(autoincrement)
        self.trademark = trademark
        self.producer = producer

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __delete__(self, instance):
        del instance.id
