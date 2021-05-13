## Функциональные тесты

После каждого теста фикстура удаляет кэш redis

## Запуск

Для запуска тестов подходят следующие команды:

Билд + запуск:

    $ sudo docker-compose -f docker-compose.yml  up -d --build

Только запуск:

    $ sudo docker-compose up tests

Остановка:

    $ sudo docker-compose -f docker-compose.yml down
   
