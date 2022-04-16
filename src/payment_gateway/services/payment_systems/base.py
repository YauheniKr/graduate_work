from models import Invoice

from .models import CheckoutInfo


class PaymentSystem:

    async def create_checkout(self, invoice: Invoice) -> CheckoutInfo:
        url = 'https://example.com/checkout'
        return CheckoutInfo(
            checkout_url=url
        )
