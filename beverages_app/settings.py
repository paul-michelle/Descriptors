import sqlite3

DATABASES = {
    "DEFAULT": "beverages",
}
DB_CONNECTION = sqlite3.connect(DATABASES["DEFAULT"])
