import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.results import ResultTimeout

from settings import RABBITMQ_URL

broker = RabbitmqBroker(url=RABBITMQ_URL)
dramatiq.set_broker(broker)


def should_retry(retries_so_far, exception):
    return retries_so_far < 3 and not (isinstance(exception, TimeLimitExceeded) or isinstance(exception, ResultTimeout))


@dramatiq.actor(queue_name='mazan_game_test', max_retries=3, time_limit=180000, retry_when=should_retry)
def game_info(url):
    pass