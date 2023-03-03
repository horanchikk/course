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
