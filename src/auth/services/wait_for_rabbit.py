import logging
from time import sleep

from core.config import settings
from db.subscriber import Subscriber, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_rabbit_availability():
    while True:
        try:
            subscriber = Subscriber(settings.RMQ_QUEUE, settings.RMQ_KEY, config)
            logger.info("RabbitMQ Running")
            exit(0)
        except Exception as e:
            logger.info(e)
            logger.error("Rabbit is not available. Sleep for 10 sec")
            sleep(10)
        else:
            subscriber.__dir__()
            exit(1)


if __name__ == '__main__':
    check_rabbit_availability()
