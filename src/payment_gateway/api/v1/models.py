import uuid
from datetime import datetime
from typing import Optional

from models import Invoice
from pydantic import BaseModel


class ResponseInvoice(BaseModel):
    id: uuid.UUID
    state: str
    created_at: datetime

    @classmethod
    def from_db_model(cls, obj: Invoice) -> None:
        return cls(
            id=obj.id,
            state=obj.state.name,
            created_at=obj.created_at,
        )


class InvoiceRequest(BaseModel):
    product_name: str = 'subscription, 1 month'
    product_count: int = 2
    product_price_currency: str = 'USD'
    product_unit_price: float = 10

    success_url: Optional[str] = None
    cancel_url: Optional[str] = None

    def to_db_model(self) -> Invoice:
        return Invoice(
            product_name=self.product_name,
            product_count=self.product_count,
            product_price_currency=self.product_price_currency,
            product_price_amount_total=self.product_unit_price * self.product_count,
        )


class ResponseInvoiceWithCheckout(BaseModel):
    invoice: ResponseInvoice
    checkout_url: str
