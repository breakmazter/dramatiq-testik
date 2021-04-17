import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.results import ResultTimeout, Results
from dramatiq.results.backends import RedisBackend

from settings import *

broker = RabbitmqBroker(url=RABBITMQ_URL)
dramatiq.set_broker(broker)


def should_retry(retries_so_far, exception):
    return retries_so_far < 3 and not (isinstance(exception, TimeLimitExceeded) or isinstance(exception, ResultTimeout))


@dramatiq.actor(store_results=False, queue_name='game_links', max_retries=3, time_limit=180000, retry_when=should_retry)
def game_links(url):
    pass


@dramatiq.actor(store_results=True, queue_name='game_info', max_retries=3, time_limit=180000, retry_when=should_retry)
def game_info(url):
    pass
