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

## Running playgrounds

```sh
cd checkout-api
pipenv install
pipenv shell
pipenv run python3 manage.py migrate # Run migrations
pipenv run python3 manage.py createsuperuser --email admin@example.com --username admin
pipenv run python3 manage.py runserver 8000
pipenv run python3 manage.py test checkout
```

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