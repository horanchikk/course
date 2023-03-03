# -*- coding: utf-8 -*-
from fastapi import FastAPI

from ..database import cur, db
from ..models import CreateSession


session = FastAPI()


@session.post('/')
async def create_new_session(data: CreateSession):
    """Creates a new session"""
    cur.execute(
        'INSERT INTO session (title, description, age_lim, imageUrl, date, price) '
        'VALUES (?, ?, ?, ?, ?, ?)',
        (data.name, data.description, data.age_lim, data.imageUrl, data.date, data.price)
    )
    db.commit()
    return {'response': {
        'id': cur.lastrowid
    }}


@session.get('/id{session_id}')
async def get_session_by_id(session_id: int):
    s = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if s is None:
        return {'error': 'session does not exists'}
    age = cur.execute('SELECT * FROM age_lim WHERE id = ?', (s[5],)).fetchone()
    return {'response': {
        'id': session_id,
        'title': s[1],
        'description': s[2],
        'imageUrl': s[3],
        'price': s[4],
        'age_limit': age[1],
        'date': s[6]
    }}


@session.get('/last')
async def get_last_sessions(count: int = 5):
    s = cur.execute('SELECT * FROM session ORDER BY id DESC LIMIT ?', (count,)).fetchall()
    result = []
    for i in s:
        age = cur.execute('SELECT * FROM age_lim WHERE id = ?', (i[5],)).fetchone()
        result.append({
            'id': i[0],
            'title': i[1],
            'description': i[2],
            'imageUrl': i[3],
            'price': i[4],
            'age_limit': age[1],
            'date': i[6]
        })
    return {'response': {
        'items': result,
        'size': len(result)
    }}

