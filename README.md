# Checkout API

Checkout API

## Requirements

- Python >= 3.7.6

## Version

1.0.0

## Installation

Download zip file and extract it [latest release](https://github.com/reysmerwvr/checkout-api). Or clone the repository and cd into it.

checkout-api uses a number of open source projects to work properly:

- [Python] - Python
- [pipenv] - Pipenv: Python Development Workflow for Humans
- [mysql-client] - mysqlclient

## Running it without Docker

```sh
cd checkout-api
cp .env.example .env # If you don't have .env file you can use the example one. Just rename .env.example to .env. Enter your configuration here.
pipenv install
pipenv shell
pipenv run python manage.py migrate # Run migrations
pipenv run python manage.py createsuperuser --email admin@example.com --username admin
pipenv run python manage.py runserver 8000
```

## Running it with Docker

```sh
cd checkout-api
cp .env.example .env # If you don't have .env file you can use the example one. Just rename .env.example to .env. Enter your configuration here.
docker-compose build
docker-compose -f docker-compose.yml up -d
docker-compose down -v # Bring down the development containers (and the associated volumes with the -v flag)
```

## Postman Collection

This collection contains API Docs

[Postman Collection](https://www.getpostman.com/collections/5a6d44f684d5c13e81b2)

## Postman Environment

Import checkout-api/Checkout.postman_environment.json into your postman environments

## Meta

Reysmer Valle – [@ReysmerWVR]

## License

Checkout API is (c) 2020 Reysmer Valle ([@ReysmerWVR]) and may be freely distributed under the [license-url](https://github.com/reysmerwvr/checkout-api/tree/master/LICENSE). See the `MIT-LICENSE` file.

### Todos

- Write tests
- Add code comments

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does 
its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Python]: <https://www.python.org/>
   [pipenv]: <https://pypi.org/project/pipenv/>
   [mysql-client]: <https://pypi.org/project/mysqlclient/>
   [@ReysmerWVR]: <http://twitter.com/ReysmerWVR>