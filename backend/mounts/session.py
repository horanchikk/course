# -*- coding: utf-8 -*-
from fastapi import FastAPI

from ..database import cur, db
from ..models import CreateSession


session = FastAPI()


@session.post('/')
async def create_new_session(data: CreateSession):
    """Creates a new session"""
    cur.execute(
        'INSERT INTO session (title, description, age_lim, imageUrl, date, price, ticket_count) '
        'VALUES (?, ?, ?, ?, ?, ?, ?)',
        (data.name, data.description, data.age_lim, data.imageUrl, data.date, data.price, data.ticket_count)
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
        'date': s[6],
        'ticket_count': s[7]
    }}


@session.patch('/id{session_id}')
async def edit_session(
        session_id: int,
        title: str = None,
        image_url: str = None,
        price: int = None,
        ticket_count: int = None
):
    """Edits session"""
    s = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if s is None:
        return {'error': 'this session does not exists'}
    title = title if title else s[1]
    image_url = image_url if image_url else s[3]
    price = price if price else s[4]
    ticket_count = ticket_count if ticket_count else s[7]
    cur.execute('UPDATE session SET title = ?, imageUrl = ?, price = ?, ticket_count = ? WHERE id = ?',
                (title, image_url, price, ticket_count, session_id))
    db.commit()
    return {'response': 'success'}


@session.get('/last')
async def get_last_sessions(count: int = 5):
    s = cur.execute('SELECT * FROM session ORDER BY id DESC LIMIT ?', (count,)).fetchall()
    result = []
    for i in s:
        age = cur.execute('SELECT * FROM age_lim WHERE id = ?', (i[5],)).fetchone()
        result.append({
            'id': i[0],
            'title': i[1],
            'imageUrl': i[3],
            'age_limit': age[1],
            'date': i[6],
            'ticket_count': i[7]
        })
    return {'response': {
        'items': result,
        'size': len(result)
    }}


@session.get('/')
async def get_sessions(offset: int = 0, count: int = 5):
    """Retrieves sessions"""
    s = cur.execute('SELECT * FROM session WHERE id > ? LIMIT ?', (offset, count,)).fetchall()
    result = []
    for i in s:
        age = cur.execute('SELECT * FROM age_lim WHERE id = ?', (i[5],)).fetchone()
        result.append({
            'id': i[0],
            'title': i[1],
            'imageUrl': i[3],
            'price': i[4],
            'age_limit': age[1],
            'date': i[6],
            'ticket_count': i[7]
        })
    return {'response': {
        'items': result,
        'size': len(result)
    }}


@session.patch('/genres{session_id}')
async def add_genres(session_id: int, genre_id: int):
    """Adds a new genres into session"""
    s = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if s is None:
        return {'error': 'sessions does not exists'}
    g = [
        i[1] for i in
        cur.execute('SELECT * FROM session_genre WHERE session_id = ?', (session_id,)).fetchall()
    ]
    if genre_id in g:
        return {'error': 'session already have this genre'}
    cur.execute('INSERT INTO session_genre (genre_id, session_id) VALUES (?, ?)', (genre_id, session_id))
    db.commit()
    return {'response': {
        'id': cur.lastrowid
    }}


@session.get('/genres{session_id}')
async def get_genres(session_id: int):
    """Retrieves all genres of the session"""
    s = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if s is None:
        return {'error': 'sessions does not exists'}
    g = [
        cur.execute('SELECT * FROM genre WHERE id = ?', (i[1],)).fetchone()[1]  # title
        for i in
        cur.execute('SELECT * FROM session_genre WHERE session_id = ?', (session_id,)).fetchall()
    ]
    return {'response': {
        'items': g,
        'size': len(g)
    }}


@session.delete('/id{session_id}/genre{genre_id}')
async def delete_genre_from_session(session_id: int, genre_id: int):
    """Deletes genre from session by it IDs"""
    s = cur.execute('SELECT * FROM session_genre WHERE session_id = ? and genre_id = ?', (session_id, genre_id)).fetchone()
    if s is None:
        return {'error': 'this session has not this genre'}
    cur.execute('DELETE FROM session_genre WHERE session_id = ? and genre_id = ?', (session_id, genre_id))
    db.commit()
    return {'response': 'success'}


@session.delete('/id{session_id}')
async def delete_session_by_id(session_id: int):
    """Deletes session by ID"""
    s = cur.execute('SELECT * FROM session WHERE id = ?', (session_id,)).fetchone()
    if s is None:
        return {'error': 'this session does not exists'}
    cur.execute('DELETE FROM session WHERE id = ?', (session_id,))
    db.commit()
    return {'response': 'success'}
