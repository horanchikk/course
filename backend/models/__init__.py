# -*- coding: utf-8 -*-
from pydantic import BaseModel


class UserRegistration(BaseModel):
    role: int
    login: str
    password: str
    name: str
    surname: str
    patronymic: str
    email: str


class CreateSession(BaseModel):
    imageUrl: str
    name: str
    description: str
    date: int  # timestamp
    age_lim: int  # age limit
    price: int
    ticket_count: int


class CreateGenre(BaseModel):
    title: str
