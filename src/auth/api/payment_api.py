import json
import logging
from http import HTTPStatus

import requests
from flask import Blueprint, request
from flask_restful import Api, Resource

from db.global_init import create_session
from services.payment import Payment, UserInvoiceUpdate

payment_blueprint = Blueprint('payment', __name__)
payment_api = Api(payment_blueprint, prefix='/api/v1/')


logger = logging.getLogger(__name__)


def user_invoice_update(channel, method, properties, body, userdata=None):
    session = create_session()
    user_invoice = UserInvoiceUpdate(session)
    json_data = json.loads(body)
    user_invoice.update_invoice(json_data)


class UserPayment(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        request_id = request.headers.get('X-Request-Id')
        session = create_session()
        payment = Payment(session)
        invoice = payment.create_payment(json_data, request_id)
        data = {
            "product_name": invoice.products.product_name,
            "product_count": invoice.amount,
            "product_price_currency": invoice.products.currency,
            "product_unit_price": invoice.products.cost,
            "success_url": json_data.get("success_url"),
            "cancel_url": json_data.get("cancel_url")
        }

        test_req = requests.post(url='http://payment_gateway:8000/api/v1/invoices/', data=json.dumps(data),
                                 headers={'x-request-id': request_id})

        if test_req.status_code == HTTPStatus.OK:
            payment.add_payment_id(test_req.json(), invoice.id)
        return test_req.json().get('checkout_url')


payment_api.add_resource(UserPayment, '/payment/')
