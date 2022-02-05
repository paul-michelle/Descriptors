import os
import sqlite3
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

BASE_ENCODING = 'utf-8'

DATABASES = {
    "DEFAULT": os.path.join(BASE_DIR, "beverages"),
}
DB_CONNECTION = sqlite3.connect(DATABASES["DEFAULT"])

LOGS_FILENAME = 'beverages_logs.txt'
LOGS_LEVEL = logging.DEBUG if DEBUG else logging.INFO
