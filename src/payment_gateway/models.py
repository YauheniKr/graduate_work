import datetime
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
