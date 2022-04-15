import uuid

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models import Invoice


class ResponseInvoice(BaseModel):
    id: uuid.UUID
    created_at: Optional[datetime]

    @classmethod
    def from_db_model(cls, obj):
        return cls(
            id=obj.id,
            created_at=obj.created_at,
        )


class InvoiceRequest(BaseModel):
    product_name: str = 'subscription, 1 month'
    product_count: int = 2
    product_price_currency: str = 'USD'
    product_price_amount_total: float = 10

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
