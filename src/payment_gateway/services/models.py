import uuid

from datetime import datetime

from pydantic import BaseModel

from models import Invoice


class InvoiceStateAMPQMessage(BaseModel):
    id: uuid.UUID
    created_at: datetime
    state: str
    x_request_id: str

    @classmethod
    def from_db_model(cls, obj: Invoice):
        return cls(
            id=obj.id,
            created_at=obj.created_at,
            state=obj.state.name,
            x_request_id=obj.x_request_id,
        )
