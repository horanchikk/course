# -*- coding: utf-8 -*-
from os import path

from fastapi import FastAPI
from fastapi.responses import FileResponse


assets = FastAPI()


@assets.get('/{file:path}')
async def get_asset(file: str):
    """Returns image from assets"""
    file = f'./backend/assets/{file}'
    if path.exists(file):
        return FileResponse(file)
    return {'error': 'asset does not exists'}
