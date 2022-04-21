from typing import Optional

from models import Invoice

from .models import CheckoutInfo


class PaymentSystem:

    async def create_checkout(
        self, invoice: Invoice,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> CheckoutInfo:
        url = 'https://example.com/checkout'
        id = 'some payment id'
        return CheckoutInfo(
            checkout_id=id,
            checkout_url=url,
        )
