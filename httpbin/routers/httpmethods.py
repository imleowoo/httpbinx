# -*- coding: utf-8 -*-
from fastapi import APIRouter

router = APIRouter()


@router.delete('/delete')
async def delete():
    pass
