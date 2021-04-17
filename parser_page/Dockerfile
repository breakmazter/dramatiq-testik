FROM python:3.9.2-slim

WORKDIR /game_info

COPY game_parser_worker.py /game_info/game_parser_worker.py
COPY settings.py /game_info/settings.py
COPY requirements.txt /game_info/requirements.txt

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis, watch]'==1.10.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["dramatiq", "game_parser_worker"]