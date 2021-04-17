from re import sub

import requests
from bs4 import BeautifulSoup

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.results import ResultTimeout

from settings import *

PUN = "^\s+|\n|\r|\t|\s+$"

result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
broker = RabbitmqBroker(url=RABBITMQ_URL)
broker.add_middleware(Results(backend=result_backend))

dramatiq.set_broker(broker)


def should_retry(retries_so_far, exception):
    return retries_so_far < 3 and not (isinstance(exception, TimeLimitExceeded) or isinstance(exception, ResultTimeout))


def get_name(game_soup):
    return game_soup.find('a', {'class': 'name'}).string.strip()


def get_link(link_soup):
    return ROOT_LINK + link_soup.find('a', {'class': 'name'}).get('href')


def get_platforms(platforms_soup):
    platforms = platforms_soup.find('div', {'class': 'platforms'}).find_all('a', {'class': 'element'})
    return [platform.string.strip() for platform in platforms]


def get_tags(tags_soup):
    tags = tags_soup.find('div', {'class': 'tags'}).find_all('a', {'class': 'element'})
    return [tag.string.strip() for tag in tags]


def get_comment_count(comment_soup):
    return comment_soup.find('div', {'class': 'comments'}).find('div', {'class': 'count'}).string.strip()


@dramatiq.actor(store_results=False, queue_name='game_links', max_retries=3, time_limit=180000, retry_when=should_retry)
def game_links(url):
    """
    :param url: link of the site on which we get the data about the game
    :return: data about the game
    """
    response = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(response, "html.parser")

    game_cards = soup.find_all('div', {'class': 'game-card'})

    mass_dict_game = []
    links = []

    for game_card in game_cards:
        game_information = {'Name': get_name(game_card),
                            'Platforms': get_platforms(game_card),
                            'Tags': get_tags(game_card),
                            'Count comments': get_comment_count(game_card),
                            }

        links.append(get_link(game_card))

        mass_dict_game.append(game_information)

    return mass_dict_game, links


@dramatiq.actor(store_results=True, queue_name='game_info', max_retries=3, time_limit=180000, retry_when=should_retry)
def game_info(mass_dict_game, url):
    """
    :param mass_dict_game: company data dictionary
    :param url: link of the site on which we get the data about the game
    :return: data about the game
    """
    response = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(response, "html.parser")

    game_info_div = soup.find('div', {'class': 'game-data'}).find_all('div', {'class': ''})

    info_game = {}

    for game_inf in game_info_div:

        titles = game_inf.find_all('div', {'class': 'title'})
        values = game_inf.find_all('div', {'class': 'value'})

        info_block = {}

        for value, title in zip(values, titles):
            info_block[title.string.strip()] = sub(PUN, '', value.text)

        info_game = info_game | info_block

    return info_game | mass_dict_game
