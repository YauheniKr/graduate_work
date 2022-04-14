import uuid

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends

from pydantic import BaseModel

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import Invoice
from services.payment_systems_manager import get_payment_system

from ..utils import get_current_user_id


router = APIRouter()


class ResponseInvoice(BaseModel):
    id: uuid.UUID
    created_at: Optional[datetime]

    @classmethod
    def from_db_model(cls, obj):
        return cls(
            id=obj.id,
            created_at=obj.created_at,
        )


@router.get(
    '/',
    summary='Invoices',
    response_model=List[ResponseInvoice],
)
async def get_invoices(
    user_id: str = Depends(get_current_user_id()),
    db: AsyncSession = Depends(get_session)
):
    invoices = await db.execute(select(Invoice))
    return [
        ResponseInvoice.from_db_model(o) for o in invoices.scalars().all()
    ]


class InvoiceRequest(BaseModel):
    product_name: str = 'subscription, 1 month'
    product_count: int = 2
    product_price_currency: str = 'RUB'
    product_price_amount_total: float = 600

    def to_db_model(self):
        return Invoice(
            product_name=self.product_name,
            product_count=self.product_count,
            product_price_currency=self.product_price_currency,
            product_price_amount_total=self.product_price_amount_total,
        )


class ResponseInvoiceWithCheckout(BaseModel):
    invoice: ResponseInvoice
    checkout_url: str


@router.post(
    '/',
    summary='Create invoice',
    response_model=ResponseInvoiceWithCheckout,
)
async def create_invoice(
    invoice_request: InvoiceRequest,
    user_id: str = Depends(get_current_user_id()),
    db: AsyncSession = Depends(get_session)
):
    payment_system = get_payment_system()

    invoice = invoice_request.to_db_model()

    checkout_info = await payment_system.create_checkout(invoice)

    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return ResponseInvoiceWithCheckout(
        invoice=ResponseInvoice.from_db_model(invoice),
        checkout_url=checkout_info.checkout_url
    )
