import logging

from typing import Optional

from models import Invoice

from .base import PaymentSystem
from .models import CheckoutInfo


logger = logging.getLogger('paygateway.payments.stripe')


class StripePaymentSystem(PaymentSystem):

    async def create_checkout(
        self, invoice: Invoice,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> CheckoutInfo:
        url = 'https://stripe.com/checkout'

        if success_url:
            url = f"{url}?next={success_url}"
        return CheckoutInfo(
            checkout_url=url
        )
