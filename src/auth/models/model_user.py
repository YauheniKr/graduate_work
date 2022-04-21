import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, UniqueConstraint, Integer, CheckConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from src.models.model_base import ModelBase
from src.models.model_product import Products

import enum

from src.models.model_role import Role


class Status(enum.Enum):
    paid = 1
    unpaid = 2


class User(ModelBase):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True)
    password = Column(String(128))
    email = Column(String(70), unique=True, nullable=False)

    role = relationship(Role, secondary="role_user", backref=backref("users", lazy="dynamic", cascade='all, delete'))

    def __repr__(self):
        return f'{self.username}'


class AuthHistory(ModelBase):
    __tablename__ = "auth_history"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("user.id", ondelete="cascade"))
    timestamp = Column(DateTime, server_default=func.now())
    user_agent = Column(Text, nullable=False)
    ip_address = Column(String(20))
    device = Column(Text)


class SocialAccount(ModelBase):
    __tablename__ = 'social_account'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user = relationship(User, backref=backref('social_accounts', lazy=True))
    social_id = Column(Text, nullable=False)
    social_name = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


class UserInvoice(ModelBase):
    __tablename__ = "user_invoice"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, )
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    product_id = Column(ForeignKey('products.id'), primary_key=True)
    amount = Column(Integer, default=1)
    invoice_id = Column(UUID(as_uuid=True), unique=True, )
    payment_status = Column(Enum(Status), default=Status.unpaid)
    created_at = Column(DateTime, default=datetime.utcnow)
    request_id = Column(UUID(as_uuid=True), unique=True, )
    invoice_due_date = Column(DateTime)

    user = relationship(User, backref=backref("user", lazy=True))
    products = relationship(Products, backref=backref("products", lazy=True))

    __table_args__ = (CheckConstraint(amount > 0, name='check_amount_positive'),)
