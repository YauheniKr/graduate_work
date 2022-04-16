from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import ping
from api.v1 import invoices
from api.v1.payments import fakepaysystem

from services.invoice_states_manager import invoice_manager


app = FastAPI(
    title='PAYGATEWAY',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await invoice_manager.start()


@app.on_event('shutdown')
async def shutdown():
    await invoice_manager.stop()


app.include_router(ping.router, prefix='/api/v1/ping', tags=['ping'])
app.include_router(invoices.router, prefix='/api/v1/invoices', tags=['invoices'])
app.include_router(fakepaysystem.router, prefix='/api/v1/pyments/fake', tags=['payments'])
