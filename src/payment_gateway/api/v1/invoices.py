import uuid

from http import HTTPStatus
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Response,
    Request,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.postgres import get_session
from models import Invoice
from services.payment_systems_manager import get_payment_system

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
    response: Response,
    db: AsyncSession = Depends(get_session),
    x_request_id: str = Header(None, example=str(uuid.uuid4())),
):
    if not x_request_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="There is no x_request_id in header"
        )

    invoices = await db.execute(select(Invoice))

    response.headers["X-Request-Id"] = x_request_id

    return [
        ResponseInvoice.from_db_model(o) for o in invoices.scalars().all()
    ]


@router.post(
    '/',
    summary='Create invoice',
    response_model=ResponseInvoiceWithCheckout,
)
async def create_invoice(
    response: Response,
    invoice_request: InvoiceRequest,
    db: AsyncSession = Depends(get_session),
    x_request_id: str = Header(None, example=str(uuid.uuid4())),
):
    if not x_request_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="There is no x_request_id in header"
        )

    payment_system = get_payment_system()

    invoice = invoice_request.to_db_model()
    invoice.x_request_id = x_request_id

    checkout_info = await payment_system.create_checkout(invoice)

    db.add(invoice)

    try:
        await db.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
        )
    # await db.refresh(invoice)

    response.headers["X-Request-Id"] = x_request_id

    return ResponseInvoiceWithCheckout(
        invoice=ResponseInvoice.from_db_model(invoice),
        checkout_url=checkout_info.checkout_url
    )
