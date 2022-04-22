import uuid

from sqlalchemy import CheckConstraint, Column, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID

from models.model_base import ModelBase


class Products(ModelBase):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, )
    product_name = Column(Text(), default='subscription')
    cost = Column(Float(precision=2), default=1)
    currency = Column(String(length=3), default='USD')

    __table_args__ = (CheckConstraint(cost > 0, name='check_cost_positive'),)
