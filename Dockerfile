FROM python:3.7-alpine

LABEL version="1.0.0"
LABEL description="Checkout API Docker Image"
LABEL maintainer="Reysmer Valle <reysmerwvr@gmail.com>"

ENV PYTHON_ENV development
ENV PYTHONUNBUFFERED 1
ENV PORT 8000
ENV PROJECT_DIR /var/www/app/current

RUN mkdir -p /var/www/app/current
WORKDIR ${PROJECT_DIR}

COPY . ./var/www/app/current

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \ 
    && pip install --upgrade pipenv

EXPOSE ${PORT}

ENTRYPOINT ["./docker-entrypoint.sh"]