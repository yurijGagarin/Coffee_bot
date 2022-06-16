FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY alembic /app/alembic/
COPY alembic.ini config.py experiment.py /app/

CMD alembic upgrade head && python experiment.py
