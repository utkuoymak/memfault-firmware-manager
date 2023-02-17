FROM python:3.11-alpine

EXPOSE 8880

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn -b 0.0.0.0:8880 -w 4 wsgi:app