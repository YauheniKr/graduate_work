from .payment_systems.stripe import StripePaymentSystem


def get_payment_system():
    return StripePaymentSystem()
