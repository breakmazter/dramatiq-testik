FROM python:3.9.2-slim

WORKDIR /game_info

COPY website_worker.py /game_info/website_worker.py
COPY actors_interface.py /game_info/actors_interface.py
COPY requirements.txt /game_info/requirements.txt
COPY settings.py /game_info/settings.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, watch]'==1.10.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["python", "website_worker.py"]