FROM python:3.13-alpine

WORKDIR /application

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 2137

ENTRYPOINT flask run --debug --port 2137
