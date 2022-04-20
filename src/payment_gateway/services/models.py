import uuid
from datetime import datetime

from models import Invoice
from pydantic import BaseModel


class InvoiceStateAMPQMessage(BaseModel):
    id: uuid.UUID
    created_at: datetime
    state: str
    checkout_id: str

    @classmethod
    def from_db_model(cls, obj: Invoice):
        return cls(
            id=obj.id,
            created_at=obj.created_at,
            state=obj.state.name,
            checkout_id=obj.checkout_id

        )
