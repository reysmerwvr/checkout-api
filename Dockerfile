# pull official base image
FROM python:3.7-alpine

LABEL version="1.0.0"
LABEL description="Checkout API Docker Image"
LABEL maintainer="Reysmer Valle <reysmerwvr@gmail.com>"

# set environment variables
ENV PYTHON_ENV development
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 8000
ENV PROJECT_DIR /var/www/app/current

RUN mkdir -p /var/www/app/current
WORKDIR ${PROJECT_DIR}

COPY ./Pipfile .

RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		python3-dev \
		musl-dev \
    && pip install --upgrade pip pipenv \
    && pipenv install \
    && apk del .build-deps

# copy entrypoint.sh
COPY ./docker-entrypoint.sh .

# copy project
COPY . .

EXPOSE ${PORT}

ENTRYPOINT ["/var/www/app/current/docker-entrypoint.sh"]