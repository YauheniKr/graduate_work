from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import Invoice
from services.payment_systems_manager import get_payment_system
from services.invoice_states_manager import get_invoices_state_manager

from .models import (
    ResponseInvoice,
    InvoiceRequest,
    ResponseInvoiceWithCheckout,
)

router = APIRouter()


@router.get(
    '/',
    summary='Invoices',
    response_model=List[ResponseInvoice],
)
async def get_invoices(
    db: AsyncSession = Depends(get_session)
):
    invoices = await db.execute(select(Invoice))
    return [
        ResponseInvoice.from_db_model(o) for o in invoices.scalars().all()
    ]


@router.post(
    '/',
    summary='Create invoice',
    response_model=ResponseInvoiceWithCheckout,
)
async def create_invoice(
    invoice_request: InvoiceRequest,
    db: AsyncSession = Depends(get_session),
    state_manager=Depends(get_invoices_state_manager),
):
    payment_system = get_payment_system()

    invoice = invoice_request.to_db_model()

    await state_manager.send_invoice_state(invoice)

    checkout_info = await payment_system.create_checkout(invoice)

    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return ResponseInvoiceWithCheckout(
        invoice=ResponseInvoice.from_db_model(invoice),
        checkout_url=checkout_info.checkout_url
    )
