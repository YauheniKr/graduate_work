import stripe
from models import Invoice

from .base import PaymentSystem
from .models import CheckoutInfo
from core.settings import settings

stripe.api_key = settings.api_key


class StripePaymentSystem(PaymentSystem):

    async def create_checkout(self, invoice: Invoice) -> CheckoutInfo:
        try:
            checkout_session = stripe.checkout.Session.create(
                clien_reference_id=invoice.id,
                currency=invoice.product_price_currency,
                line_items=[
                    {
                        'price_data': {
                            'currency': invoice.product_price_currency,
                            'unit_amount': invoice.product_price_amount_total,
                            'product_data': {
                                'name': invoice.product_name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:8001' + '/success.html',
                cancel_url='http://localhost:8001' + '/cancel.html',
            )
        except Exception as exc:
            return str(exc)
        print(checkout_session.url)
        # return redirect(checkout_session.url, code=303)
        return CheckoutInfo(checkout_url=checkout_session.url)
#     )
