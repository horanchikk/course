# -*- coding: utf-8 -*-
import time
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
    if s[7] < 1:
        return {'error': 'session tickets is ended'}
    # Decrement ticket count
    cur.execute('UPDATE session SET ticket_count = ? WHERE id = ?', (s[7]-1, session_id))
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
        t = (await get_session_by_id(i[2]))['response']
        t['ticket_id'] = i[0]
        tickets.append(t)
    price = 0
    for i in tickets:
        price += i['price']
    return {'response': {
        'price': price,
        'items': tickets,
        'size': len(tickets)
    }}


@user.delete('/removeFromCart')
async def remove_ticket_from_cart(access_token: str, session_id: int, ticket_id: int):
    """Removes ticket from cart"""
    session = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if session is None:
        return {'error': 'this session does not exists'}
    u = cur.execute('SELECT * FROM user WHERE access_token = ?', (access_token,)).fetchone()
    if u is None:
        return {'error': 'this user does not exists'}
    ticket = cur.execute('SELECT * FROM ticket WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        return {'error': 'this ticket does not exists'}
    cur.execute('DELETE FROM ticket WHERE id = ?', (ticket_id,))
    cur.execute('UPDATE session SET ticket_count = ? WHERE id = ?', (session[7]+1, session_id))
    db.commit()
    return {'response': 'success'}


@user.post('/order')
async def create_order(access_token: str, password: str):
    """Creates a new order"""
    u = cur.execute('SELECT * FROM user WHERE access_token = ? and password = ?', (access_token, password)).fetchone()
    if u is None:
        return {'error': 'this user does not exists'}
    # get cart
    cart = cur.execute('SELECT * FROM cart WHERE user_id = ?', (u[0],)).fetchone()
    tickets = cur.execute('SELECT * FROM ticket WHERE cart_id = ?', (cart[0],)).fetchall()
    # Create a new order
    cur.execute('INSERT INTO cart_order (status, timestamp) VALUES (?, ?)', (1, time.time()))
    order_id = cur.lastrowid
    cur.execute('INSERT INTO order_owner (user_id, order_id) VALUES (?, ?)', (u[0], order_id))
    order_owner_id = cur.lastrowid
    for ticket in tickets:
        # Moves ticket from ticket table to ticket_order table
        cur.execute('INSERT INTO ticket_order (order_id, session_id) VALUES (?, ?)', (order_id, ticket[2]))
        cur.execute('DELETE FROM ticket WHERE id = ?', (ticket[0],))
    db.commit()
    return {'response': {
        'id': order_id
    }}


@user.get('/orders')
async def get_user_orders(access_token: str):
    """Retrieves all user's orders"""
    u = cur.execute('SELECT * FROM user WHERE access_token = ?', (access_token,)).fetchone()
    if u is None:
        return {'error': 'this user does not exists'}
    orders_ids = cur.execute('SELECT * FROM order_owner WHERE user_id = ?', (u[0],)).fetchall()
    result = []
    for order_id in orders_ids:
        oid = order_id[1]  # user ID

        tickets = cur.execute('SELECT * FROM ticket_order WHERE order_id = ?', (oid,)).fetchall()
        result.append({
            'items': [],
            'price': 0,
            'order_id': order_id[2],
            'status': cur.execute('SELECT * FROM cart_order WHERE id = ?', (order_id[2],)).fetchone()[1]
        })
        for ticket in tickets:
            # Get session data
            s = await get_session_by_id(ticket[2])
            result[-1]['items'].append(s['response'])
            result[-1]['price'] += result[-1]['items'][-1]['price']
        result[-1]['size'] = len(result[-1]['items'])
    return {'response': {
        'items': result,
        'size': len(result),
    }}


@user.get('/ordersList')
async def get_user_orders(filter_by: int = 1):
    """Retrieves all orders"""
    orders_ids = cur.execute('SELECT * FROM order_owner').fetchall()
    result = []
    for order_id in orders_ids:
        oid = order_id[1]  # user ID
        status = cur.execute('SELECT * FROM cart_order WHERE status = ? and id = ?', (filter_by, oid)).fetchone()
        if status is None:
            continue
        tickets = cur.execute('SELECT * FROM ticket_order WHERE order_id = ?', (order_id[0],)).fetchall()
        result.append({
            'items': [],
            'price': 0,
            'order_id': order_id[2],
            'status': cur.execute('SELECT * FROM cart_order WHERE id = ?', (order_id[2],)).fetchone()[1]
        })
        for ticket in tickets:
            # Get session data
            s = await get_session_by_id(ticket[2])
            result[-1]['items'].append(s['response'])
            result[-1]['price'] += result[-1]['items'][-1]['price']
        result[-1]['size'] = len(result[-1]['items'])
    return {'response': {
        'items': result,
        'size': len(result),
    }}


@user.patch('/order{order_id}')
async def update_order(order_id: int, status: int, description: str):
    """Updates order status"""
    o = cur.execute('SELECT * FROM cart_order WHERE id = ?', (order_id,)).fetchone()
    if o is None:
        return {'error': 'this order does not exists'}
    cur.execute('UPDATE cart_order SET status = ? WHERE id = ?', (status, order_id,))
    if status == 3:  # cancelation
        cur.execute('INSERT INTO order_cancel (description) VALUES (?)', (description,))
    return {'response': 'success'}


@user.delete('/order{order_id}')
async def delete_order(order_id: int):
    """Deletes order"""
    o = cur.execute('SELECT * FROM cart_order WHERE id = ?', (order_id,)).fetchone()
    if o is None:
        return {'error': 'this order does not exists'}
    cur.execute('DELETE FROM cart_order WHERE id = ?', (order_id,))
    cur.execute('DELETE FROM ticket_order WHERE order_id = ?', (order_id,))
    return {'response': 'success'}
