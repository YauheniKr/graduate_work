import datetime
import enum
import uuid

from sqlalchemy import Column
from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    String,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class InvoiceState(enum.Enum):
    unpaid = 1
    paid = 2
    failed = 3


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    state = Column(
        Enum(InvoiceState),
        default=InvoiceState.unpaid,
        nullable=False
    )

    product_name = Column(String)
    product_count = Column(Integer)
    product_price_currency = Column(String)
    product_price_amount_total = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
    )

    x_request_id = Column(String, nullable=False, unique=True)
