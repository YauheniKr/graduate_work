# import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import ping

from core import settings
# from db import elastic
# from db import redis

app = FastAPI(
    title='PAYGATEWAY',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(ping.router, prefix='/api/v1/ping', tags=['ping'])


# if __name__ == '__main__':
#     uvicorn.run(
#         'main:app',
#         host='0.0.0.0',
#         port=8001,
#     )
