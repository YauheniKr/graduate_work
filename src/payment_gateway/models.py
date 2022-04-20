import datetime
import enum
import uuid

from db.postgres import Base
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID


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
    checkout_id = Column(String, nullable=True, unique=False)
