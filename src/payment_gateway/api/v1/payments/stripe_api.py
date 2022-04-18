import json
import stripe
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from core.settings import settings

stripe.api_key = settings.api_key
endpoint_secret = settings.api_webhook_key

router = APIRouter()


@router.post('/webhook', summary='Stripe webhook')
async def webhook(request: Request):
    event = None
    data = await request.body()
    try:
        event = json.loads(data)
    except Exception as e:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': '⚠️  Webhook error while parsing basic request.' + str(e)})
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                data, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={'message': '⚠️  Webhook signature verification failed.'})

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} succeeded'.format(payment_intent['amount']))
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']  # contains a stripe.PaymentMethod
        print('✅ Payment session for {} succeeded'.format(checkout_session['amount_total']))
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'message': '⚠️  Ammm. Ok'})
