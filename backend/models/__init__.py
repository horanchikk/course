# -*- coding: utf-8 -*-
from pydantic import BaseModel


class UserRegistration(BaseModel):
    role: int
    login: str
    password: str
