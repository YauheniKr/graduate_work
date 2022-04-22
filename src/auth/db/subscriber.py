import json
import logging
import signal

import pika

from api.payment_api import user_invoice_update
from core.config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)

config = {'host': settings.RMQ_HOST, 'port': settings.RMQ_PORT, 'exchange': settings.RMQ_EXCHANGE}


def exit_handler(signal, frame):
    logger.info('signal exit received. stopping consuming')
    sys.exit(0)


signal.signal(signal.SIGINT, exit_handler)


class Subscriber:
    def __init__(self, queueName, bindingKey, config):
        self.queueName = queueName
        self.bindingKey = bindingKey
        self.config = config
        self.connection = self._create_connection()

    def __del__(self):
        self.connection.close()

    def _create_connection(self):
        parameters = pika.ConnectionParameters(host=self.config['host'], port=self.config['port'])
        return pika.BlockingConnection(parameters)

    def setup(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')
        channel.queue_declare(queue=self.queueName)
        channel.queue_bind(queue=self.queueName, exchange=self.config['exchange'], routing_key=self.bindingKey)
        logger.info('start read message from queue')
        channel.basic_consume(queue=self.queueName,
                              on_message_callback=user_invoice_update, auto_ack=False)
        channel.start_consuming()


def main():
    """Main method."""
    logger.error(config)
    subscriber = Subscriber(settings.RMQ_QUEUE, settings.RMQ_KEY, config)
    subscriber.setup()


if __name__ == '__main__':
    main()
