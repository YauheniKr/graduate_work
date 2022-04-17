from .payment_systems.stripe_service import StripePaymentSystem


def get_payment_system():
    return StripePaymentSystem()
