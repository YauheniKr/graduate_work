import uuid

from db.postgres import get_session
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models import Invoice, InvoiceState
from pydantic import BaseModel
from services.invoice_states_manager import get_invoices_state_manager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()


class ResponseInvoiceWithCheckout(BaseModel):
    invoice_guid: uuid.UUID
    state: str = 'paid'


@router.post('/webhook', summary='Test payment webhook')
async def set_payment_state(
    data: ResponseInvoiceWithCheckout,
    db: AsyncSession = Depends(get_session),
    state_manager=Depends(get_invoices_state_manager),
):
    invoices = await db.execute(select(Invoice).where(Invoice.id == data.invoice_guid))
    invoice = invoices.one()[0]

    if data.state == 'paid':
        invoice.state = InvoiceState.paid

    db.add(invoice)
    await db.commit()

    await state_manager.send_invoice_state(invoice)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
    )
