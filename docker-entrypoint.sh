#!/bin/sh

if [ "$DB_CONNECTION" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "MySQL started"
fi

pipenv run python manage.py flush --no-input
pipenv run python manage.py migrate

exec "$@"