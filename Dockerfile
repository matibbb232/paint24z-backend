FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add libpq-dev dos2unix
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

COPY ./entrypoint.sh ./app

# fixing windows stuff
RUN ["dos2unix", "/app/entrypoint.sh"]
RUN ["chmod", "+rx", "/app/entrypoint.sh"]

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

EXPOSE 8000
