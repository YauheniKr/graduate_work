from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/', summary='Ping')
async def add_task():
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Pong'},
    )
