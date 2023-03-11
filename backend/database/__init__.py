# -*- coding: utf-8 -*-
from sqlite3 import connect


db = connect('nnf.db')
cur = db.cursor()

# Users
cur.execute('''CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role INTEGER NOT NULL,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    login TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    access_token TEXT NOT NULL  -- unique token
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
# Order
cur.execute('''CREATE TABLE IF NOT EXISTS cart_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status INTEGER NOT NULL,
    timestamp INTEGER NOT NULL
);''')
# Order status
cur.execute('''CREATE TABLE IF NOT EXISTS order_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);''')
# Order cancel description
cur.execute('''CREATE TABLE IF NOT EXISTS order_cancel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);''')
# Tickets
cur.execute('''CREATE TABLE IF NOT EXISTS ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL
);''')
# Tickets in order
cur.execute('''CREATE TABLE IF NOT EXISTS ticket_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL
);''')
# Genres, only for admins
cur.execute('''CREATE TABLE IF NOT EXISTS genre (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);''')
# Sessions
cur.execute('''CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    imageUrl TEXT NOT NULL,
    price INTEGER NOT NULL,
    age_lim INTEGER NOT NULL,
    date INTEGER NOT NULL,  -- timestamp
    ticket_count INTEGER NOT NULL
);''')
# Age limit
cur.execute('''CREATE TABLE IF NOT EXISTS age_lim (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER NOT NULL
);''')
# Session's genres
cur.execute('''CREATE TABLE IF NOT EXISTS session_genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL
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

default(
    'user', 1,
    {
        'role': 1,
        'name': 'biba',
        'surname': 'boba',
        'patronymic': 'asdasd',
        'login': 'admin',
        'email': 'secure...',
        'password': 'admin66',
        'access_token': 'longlonglongtoken'
    }
)

default(
    'genre', 4,
    {'title': 'Комедия'},
    {'title': 'Ужасы'},
    {'title': 'Приключения'},
    {'title': 'Фентези'},
)

default(
    'age_lim', 5,
    {'age': 0},  # 0+, ID: 1
    {'age': 12},  # 12+, ID: 2
    {'age': 16},  # etc.
    {'age': 18},
    {'age': 21},
)

default(
    'order_status', 3,
    {'title': 'Новый'},
    {'title': 'Подтвержденный'},
    {'title': 'Отмененный'},
)
