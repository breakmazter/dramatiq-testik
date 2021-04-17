# CONFIGS FOR RABBITMQ
QUEUE_DRIVER = 'rabbitmq'
RABBITMQ_HOST = '34.94.7.254'
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = '/'
RABBITMQ_LOGIN = 'mazan'
RABBITMQ_PASSWORD = 'mazan'

RABBITMQ_URL = f'''amqp://{RABBITMQ_LOGIN}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'''
RABBITMQ_SCOCKET_TIMEOUT = 10
RABBITMQ_HEARTBEAT = 0

# CONFIGS FOR REDIS
REDIS_HOST = '34.83.238.11'
REDIS_PORT = 6379
REDIS_USERNAME = 'user'
REDIS_PASSWORD = 'LYWxyNDJSg7h'
REDIS_URL = f'''redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'''

# CONFIGS FOR PARSING
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}


ROOT_LINK = "https://www.igromania.ru"
