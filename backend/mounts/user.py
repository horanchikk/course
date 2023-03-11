# -*- coding: utf-8 -*-
from secrets import token_hex

from fastapi import FastAPI

from ..models import UserRegistration
from ..database import db, cur
from .session import get_session_by_id


user = FastAPI()


@user.post('/reg')
async def register(data: UserRegistration):
    """User registration

    Retrieves access token when successfully registered
    """
    u = cur.execute(
        'SELECT * FROM user WHERE login = ? or email = ?', (data.login, data.email)
    ).fetchone()
    if u is not None:
        return {'error': 'login or email already used'}
    roles = [i[0] for i in cur.execute('SELECT * FROM role').fetchall()]
    if data.role not in roles:
        return {'error': 'this role does not exists'}
    token = token_hex(24)
    cur.execute(
        'INSERT INTO user (role, login, password, name, surname, patronymic, email, access_token) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (data.role, data.login, data.password, data.name, data.surname, data.patronymic, data.email, token)
    )
    # Register user cart
    user_id = cur.lastrowid
    cur.execute('INSERT INTO cart (user_id) VALUES (?);', (user_id,))
    db.commit()
    return {'response': {'access_token': token}}


@user.get('/login')
async def log_in(login: str, password: str):
    """User authentication

    Retrieves access token when successfully logged in
    """
    u = cur.execute('SELECT * FROM user WHERE login = ? and password = ?', (login, password)).fetchone()
    if u is None:
        return {'incorrect login or password!'}
    return {'response': {'access_token': u[8]}}


@user.patch('/addToCart{user_id}')
async def add2cart(user_id: int, session_id: int):
    """Adds session to cart if available"""
    s = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if s is None:
        return {'error': 'this session does not exists'}
    # Check if session tickets is less than one
    if s[9] < 1:
        return {'error': 'session tickets is ended'}
    # Decrement ticket count
    cur.execute('UPDATE session SET ticket_count = ? WHERE id = ?', (s[9]-1, session_id))
    # Add ticket into cart
    cart = cur.execute('SELECT * FROM cart WHERE user_id = ?', (user_id,)).fetchone()
    cur.execute('INSERT INTO ticket (cart_id, session_id) VALUES (?, ?)', (cart[0], session_id))
    db.commit()
    return {'response': {
        'id': cur.lastrowid
    }}


@user.get('/')
async def get_user(access_token: str):
    """Retrieves user by its token"""
    u = cur.execute('SELECT * FROM user WHERE access_token = ?', (access_token,)).fetchone()
    if u is None:
        return {'error': 'this user does not exists'}
    role = cur.execute('SELECT * FROM role WHERE id = ?', (u[1],)).fetchone()
    return {'response': {
        'id': u[0],
        'role': role[1],
        'name': u[2],
        'surname': u[3],
        'patronymic': u[4],
        'login': u[5],
        'email': u[6]
    }}


@user.get('/cart')
async def get_user_cart(access_token: str):
    """Retrieves user cart by user's token"""
    s = cur.execute('SELECT * FROM user WHERE access_token = ?', (access_token,)).fetchone()
    if s is None:
        return {'error': 'this user does not exists'}
    # get cart ID
    cart = cur.execute('SELECT * FROM cart WHERE user_id = ?', (s[0],)).fetchone()
    tickets = []
    # get all tickets from cart
    result = cur.execute('SELECT * FROM ticket WHERE cart_id = ?', (cart[0],)).fetchall()
    for i in result:
        # get session
        tickets.append((await get_session_by_id(i[2]))['response'])
    price = 0
    for i in tickets:
        price += i['price']
    return {'response': {
        'price': price,
        'items': tickets,
        'size': len(tickets)
    }}


@user.delete('/removeFromCart')
async def remove_ticket_from_cart(access_token: str, session_id: int):
    """Removes ticket from cart"""
    session = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if session is None:
        return {'error': 'this session does not exists'}
    user = cur.execute('SELECT * FROM user WHERE access_token = ?', (access_token,)).fetchone()
    if user is None:
        return {'error': 'this user does not exists'}
    cart = cur.execute('SELECT * FROM cart WHERE user_id = ?', (user[0],)).fetchone()
    ticket = cur.execute('SELECT * FROM ticket WHERE session_id = ? and cart_id = ?', (session_id, cart[0])).fetchone()
    if ticket is None:
        return {'error': 'this ticket does not exists'}
    cur.execute('DELETE FROM ticket WHERE session_id = ? and cart_id = ?', (session_id, cart[0]))
    cur.execute('UPDATE session SET ticket_count = ? WHERE id = ?', (session[9]+1, session_id))
    db.commit()
    return {'response': 'success'}
