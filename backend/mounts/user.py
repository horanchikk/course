# -*- coding: utf-8 -*-
from secrets import token_hex

from fastapi import FastAPI

from ..models import UserRegistration
from ..database import db, cur


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
        return {'error': 'login already used'}
    roles = [i[0] for i in cur.execute('SELECT * FROM role').fetchall()]
    if data.role not in roles:
        return {'error': 'this role does not exists'}
    token = token_hex(24)
    cur.execute(
        'INSERT INTO user (role, login, password, access_token, name, surname, patronymic, email) VALUES (?, ?, ?, ?)',
        (data.role, data.login, data.password, token, data.name, data.surname, data.patronymic, data.email)
    )
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
    return {'response': {'access_token': u[4]}}
