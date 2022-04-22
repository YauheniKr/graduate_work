import datetime
import logging

from dateutil.relativedelta import relativedelta
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import and_, desc, update

from models.model_user import UserInvoice

logger = logging.getLogger(__name__)


class Payment:

    def __init__(self, session):
        self.session = session

    @jwt_required()
    def create_payment(self, json_data, request_id):
        user_id = get_jwt()['sub']
        user_invoice = UserInvoice(
            user_id=user_id,
            product_id=json_data.get('product_id'),
            amount=json_data.get('product_count'),
            request_id=request_id
        )
        self.session.add(user_invoice)
        self.session.commit()
        return user_invoice

    def add_payment_id(self, json_data, invoice):
        user_invoice = self.session.execute(
            update(UserInvoice).where(
                UserInvoice.id == invoice
            ).values(
                invoice_id=json_data.get('invoice').get('id'),
            )
        )
        self.session.commit()

        if user_invoice == 0:
            return None

        invoice = self.session.query(UserInvoice).filter_by(id=invoice).first()
        return invoice


class UserInvoiceUpdate:

    def __init__(self, session):
        self.session = session

    def update_invoice(self, body):
        logger.info('read message from queue and update db')
        invoice = self.session.query(UserInvoice).filter(UserInvoice.invoice_id == body['id']).first()

        if invoice is None:
            return None

        invoice.payment_status = body.get('state')
        self.session.add(invoice)
        self.session.commit()

        latest_payment = self._get_user_payment(invoice.user_id).first()

        if latest_payment is None:
            latest_payment = invoice

        period = invoice.amount * relativedelta(months=1)

        if latest_payment.invoice_due_date is None or latest_payment.invoice_due_date < datetime.datetime.now():
            due_date = datetime.datetime.now() + period
        else:
            due_date = latest_payment.invoice_due_date + period

        invoice.invoice_due_date = due_date
        self.session.add(invoice)
        self.session.commit()
        self.session.close()

        return invoice

    def _get_user_payment(self, user_id):
        latest_user_payment = self.session.query(
            UserInvoice
        ).filter(
            and_(
                UserInvoice.user_id == user_id,
                UserInvoice.payment_status == 'paid',
                UserInvoice.invoice_due_date.is_not(None),
            )
        ).order_by(desc(UserInvoice.invoice_due_date))

        return latest_user_payment
