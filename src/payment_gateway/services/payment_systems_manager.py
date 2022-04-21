from .payment_systems.base import PaymentSystem
from .payment_systems.stripe_service import StripePaymentSystem


def get_payment_system() -> PaymentSystem:
    return StripePaymentSystem()
