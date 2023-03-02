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
