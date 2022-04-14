import aio_pika

from aio_pika import Message

from core.settings import settings
from models import Invoice


class InvoiceStatesManager:
    def __init__(self):
        self.queue_name = "test_queue"
        self.routing_key = "test_queue"

    # TODO
    async def send_invoice_state(self, invoice: Invoice):
        connection = await aio_pika.connect_robust(
            settings.rabbitmq_uri,
        )
        async with connection:

            # Creating channel
            channel = await connection.channel()

            # Declaring exchange
            exchange = await channel.declare_exchange("direct", auto_delete=True)

            # Declaring queue
            queue = await channel.declare_queue(self.queue_name, auto_delete=True)

            # # Binding queue
            await queue.bind(exchange, self.routing_key)

            await exchange.publish(
                Message(
                    bytes("Hello", "utf-8"),
                    content_type="text/plain",
                    headers={"foo": "bar"},
                ),
                'test_queue',
            )

            # await queue.unbind(exchange, self.routing_key)
            # await queue.delete()
            await connection.close()


async def get_invoices_state_manager():
    yield InvoiceStatesManager()
