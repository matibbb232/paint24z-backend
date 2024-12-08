FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add libpq-dev
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

COPY ./entrypoint.sh ./app
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

EXPOSE 8000
