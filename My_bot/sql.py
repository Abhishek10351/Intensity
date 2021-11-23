

import sqlite3
connector = sqlite3.connect("db.sqlite3")
cursor = connector.cursor()
def execute(*query):
    cursor.execute(*query)
    connector.commit()


def fetch(*query):
    cursor.execute(*query)
    return cursor.fetchone()


def fetchall(*query):
    cursor.execute(*query)
    return cursor.fetchall()
