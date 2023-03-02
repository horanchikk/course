# -*- coding: utf-8 -*-
from sqlite3 import connect


db = connect('nnf.db')
cur = db.cursor()

# Users
cur.execute('''CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role INTEGER NOT NULL,
    login TEXT NOT NULL,
    password TEXT NOT NULL
);''')
# Roles
cur.execute('''CREATE TABLE IF NOT EXISTS role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);''')
# Cart
cur.execute('''CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL  -- cart owner (client)
);''')
# Tickets
cur.execute('''CREATE TABLE IF NOT EXISTS ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL
);''')
# Genres, only for admins
cur.execute('''CREATE TABLE IF NOT EXISTS genre (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);''')
# Sessions
cur.execute('''CREATE TABLE IF NOT EXISTS session(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    imageUrl TEXT NOT NULL,
    genre INTEGER NOT NULL  -- bit flag, keep some genres in it
);''')

db.commit()


# Default values
def default(table: str, max_size: int, *rows: dict[str, object]):
    """Initializes default values for db

    :param table: table name
    :param max_size: max table length
    :param rows: varargs of rows
    """
    size = len(cur.execute(f'SELECT * FROM {table}').fetchall())
    if size < max_size:
        for row in rows:
            keys = [key for key in row]
            cur.execute(
                f'INSERT INTO {table} ({", ".join(keys)}) VALUES ({", ".join(["?" for i in keys])})',
                tuple([row[key] for key in keys])
            )
        db.commit()


default(
    'role', 3,
    {'title': 'Администратор'},
    {'title': 'Посетитель сайта'},
    {'title': 'Клиент'}
)
