import logging

from typing import Optional

import stripe
from core.settings import settings
from models import Invoice

from .base import PaymentSystem
from .models import CheckoutInfo

stripe.api_key = settings.api_key
logger = logging.getLogger('paygateway.services.payment_systems.stripe')


class StripePaymentSystem(PaymentSystem):

    async def create_checkout(
        self, invoice: Invoice,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> CheckoutInfo:

        checkout_line_items = [
            {
                'price_data': {
                    'currency': invoice.product_price_currency,
                    'unit_amount': int(invoice.product_price_amount_total * 100),
                    'product_data': {
                        'name': invoice.product_name,
                    },
                },
                'quantity': 1,
            },
        ]
        try:
            logger.debug(f'INVOICE ID IS: {invoice.id}')
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=invoice.id,
                line_items=checkout_line_items,
                mode='payment',
                # FIXME: изменить ссылка на указанные в ручке
                success_url='http://localhost:8001/success.html',
                cancel_url='http://localhost:8001/cancel.html',
            )
        except Exception as exc:
            logger.error(f'Checkout session error: {exc}')
            raise exc
        logger.debug(f'Checkout URL LINK: {checkout_session.url}')
        return CheckoutInfo(
            checkout_id=checkout_session.stripe_id,
            checkout_url=checkout_session.url,
        )
