from typing import NoReturn

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def already_exist(subject: str) -> NoReturn:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'{subject} already exist')


def not_found(subject: str) -> NoReturn:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'{subject} not found')


def success_delete(subject: str) -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={'status': True,
                                 'message': f'The {subject} has been deleted'})
