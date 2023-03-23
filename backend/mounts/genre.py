# -*- coding: utf-8 -*-
from fastapi import FastAPI

from ..database import db, cur
from ..models import CreateGenre


genre = FastAPI()


@genre.post('/')
async def create_new_genre(data: CreateGenre):
    """Creates a new genre

    Retrieves id when successfully created
    """
    cur.execute('INSERT INTO genre (title) VALUES (?)', (data.title,))
    db.commit()
    return {'response': {
        'id': cur.lastrowid
    }}


@genre.get('/')
async def get_all_genres():
    g = cur.execute('SELECT * FROM genre').fetchall()
    arr = [{
        'id': i[0],
        'title': i[1]
    } for i in g]
    return {'response': {
        'items': arr,
        'size': len(arr)
    }}


@genre.delete('/id{genre_id}')
async def create_new_genre(genre_id: int):
    """Creates a new genre

    Retrieves id when successfully created
    """
    cur.execute('DELETE FROM genre WHERE id = ?', (genre_id,))
    db.commit()
    return {'response': 'success'}
