# Техническое задание

Предлагается выполнить проект «Асинхронное API». Этот сервис будет точкой входа для всех клиентов. В первой итерации в сервисе будут только анонимные пользователи. Функции авторизации и аутентификации запланированы в модуле «Auth».

## Используемые технологии

- Код приложения пишется на **Python + FastAPI**.
- Приложение запускается под управлением сервера **ASGI**(uvicorn).
- Хранилище – **ElasticSearch**.
- За кеширование данных отвечает – **redis**.
- Все компоненты системы запускаются через **docker**.


## Настройка

Для корректного запуска проекта необходимо произвести ряд действий.
1. Создать к корне проекта папки .es-data, .pg-data, и выдать на них права:

        $ mkdir .es-data .pg-data \
        && chmod g+rwx .es-data .pg-data \
        && chgrp 1000 .es-data .pg-data

2. Отредактировать файл .env (на этот раз залил в гит) можно вбить свои настройки или оставить как есть.

**[ Postgresql ]**
```
POSTGRES_USER = django_admin 
POSTGRES_DB = movie_admin
POSTGRES_PASSWORD = 1234
TZ='Europe/Moscow'
```
**[ init.sh ]**
```
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

**[ elasticsearch ]**
```
ELASTICSEARCH_HOSTS=http://elasticsearch:9200
```
**[ redis ]**
```
REDIS_HOST=redis
```

## Запуск

Для запуска контейнеров в корне проекта выполняем:

Билд + запуск:

    $ sudo docker-compose -f docker-compose.yml up -d --build

Только запуск:

    $ sudo docker-compose -f docker-compose.yml up --d

Остановка:

    $ sudo docker-compose -f docker-compose.yml down


## Тесты

Для запуска тестов локально, потребуется добавить локальные переменные:

```
export ELASTIC_HOST=localhost:9200
export FASTAPI_HOST=http://localhost:8000
export REDIS_HOST=localhost
export REDIS_PORT=6379
```

А так же установить все необходимые библиотеки на локальную машину:

```
pip install -r tests/functional/requirements.txt
```

Больше информации [тут](./tests/functional/README.md)