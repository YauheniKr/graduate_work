from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import ping
from api.v1 import invoices


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
app.include_router(invoices.router, prefix='/api/v1/invoices', tags=['invoices'])
