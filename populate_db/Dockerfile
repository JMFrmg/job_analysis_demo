FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY . /app

RUN pip3 install -r requirements.txt

#EXPOSE 8501

CMD ["python", "populate.py"]