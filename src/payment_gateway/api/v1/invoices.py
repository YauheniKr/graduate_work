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
async def get_invoices(db: AsyncSession = Depends(get_session)):
    invoices = await db.execute(select(Invoice))
    return [
        ResponseInvoice.from_db_model(o) for o in invoices.scalars().all()
    ]


class ResponseInvoiceWithCheckout(BaseModel):
    invoice: ResponseInvoice
    checkout_url: str


@router.post(
    '/',
    summary='Create invoice',
    response_model=ResponseInvoiceWithCheckout,
)
async def create_invoice(db: AsyncSession = Depends(get_session)):
    payment_system = get_payment_system()

    invoice = Invoice()

    checkout_info = await payment_system.create_checkout(invoice)

    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return ResponseInvoiceWithCheckout(
        invoice=ResponseInvoice.from_db_model(invoice),
        checkout_url=checkout_info.checkout_url
    )
