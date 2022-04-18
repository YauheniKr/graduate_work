import json
import logging

import stripe
from core.settings import settings
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

stripe.api_key = settings.api_key
endpoint_secret = settings.api_webhook_key
logger = logging.getLogger('paygateway.api.v1.stripe')

router = APIRouter()


@router.post('/webhook', summary='Stripe webhook')
async def webhook(request: Request):
    event = None
    request_data = await request.body()
    try:
        event = json.loads(request_data)
    except Exception as exc:
        logger.error(f'⚠️  Webhook error while parsing request. {exc}')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'message': f'⚠️  Webhook error while parsing request. {exc}',
            },
        )
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                request_data, sig_header, endpoint_secret,
            )
        except stripe.error.SignatureVerificationError as exc:
            logger.error(f'⚠️  Webhook signature verification failed. {exc}')
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'message': f'⚠️ Webhook signature failed. {exc}',
                },
            )

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logger.debug(f'Payment for {payment_intent["amount"]} succeeded')
    elif event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        sum_amount = checkout_session['amount_total']
        logger.debug(
            f'✅ Payment session for {sum_amount} succeeded',
        )
    else:
        # Unexpected event type
        logger.debug(f'Unhandled event type {event["type"]}')
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': '⚠️  Ammm. Ok'},
    )
