from models import Invoice

from .base import PaymentSystem
from .models import CheckoutInfo


class StripePaymentSystem(PaymentSystem):

    async def create_checkout(self, invoice: Invoice) -> CheckoutInfo:
        url = 'https://stripe.com/checkout'
        return CheckoutInfo(
            checkout_url=url
        )
