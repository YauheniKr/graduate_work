import aio_pika
import backoff
from aio_pika import Message
from core.settings import settings
from models import Invoice

# from aio_pika.connection import Connection


from.models import InvoiceStateAMPQMessage


class InvoiceStatesManager:
    def __init__(self, ampq_uri, queue_name):
        self.ampq_uri = ampq_uri
        self.queue_name = queue_name
        self.routing_key = queue_name

    @backoff.on_exception(
        backoff.expo,
        (
            ConnectionError
        ),
        max_tries=10
    )
    async def start(self) -> None:
        self.connection = await aio_pika.connect(
            self.ampq_uri
        )

        channel = await self.connection.channel()

        await channel.declare_queue(self.queue_name, auto_delete=False)

    async def stop(self) -> None:
        await self.connection.close()

    async def send_invoice_state(self, invoice: Invoice) -> None:
        channel = await self.connection.channel()

        message = InvoiceStateAMPQMessage.from_db_model(invoice)

        await channel.default_exchange.publish(
            Message(
                bytes(message.json(), 'utf-8'),
                content_type='text/plain',
            ),
            self.routing_key,
        )


invoice_manager = InvoiceStatesManager(
    settings.rabbitmq_uri,
    settings.rabbitmq_queue,
)


def get_invoices_state_manager() -> InvoiceStatesManager:
    return invoice_manager
