import json
import logging

from http import HTTPStatus
from urllib.parse import urljoin

import requests
from flask import Blueprint, request
from flask_restful import Api, Resource

from db.global_init import create_session
from services.payment import Payment, UserInvoiceUpdate

from core.config import settings

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
        """
        Метод создает платеж
        ---
        tags:
          - UserPayment
        parameters:
          - name: Authorization
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа. Добавляем Bearer в начало токена при тестировании
          - name: body
            in: body
            schema:
              properties:
                product_id:
                  in: query
                  type: string
                  format: uuid
                  required: true
                  description: UUID продукта
                product_count:
                  type: integer
                  required: true
                  description: Количество продукта
                success_url:
                  type: string
                  required: true
                  description: Ссылка на фронт в случае успеха
                cancel_url:
                  type: string
                  required: true
                  description: Ссылка на фронт в случае неудачи

        responses:
          200:
            description: Successfully created payment
            schema:
              properties:
                checkout_url:
                  type: string
                  description: ссылка на платежную систему
          409:
            description: Невозможно создать платеж
          403:
            description: Запрос без x_request_id
          500:
            description: Внутренняя ошибка сервиса PaymentGateway
        """

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

        test_req = requests.post(
            url=urljoin(settings.PAYMENT_GATEWAY_URL, 'api/v1/invoices/'),
            data=json.dumps(data),
            headers={'x-request-id': request_id}
        )

        if test_req.status_code == HTTPStatus.OK:
            payment.add_payment_id(test_req.json(), invoice.id)
        return test_req.json().get('checkout_url')


payment_api.add_resource(UserPayment, 'payment/')
