## Запуск

Для запуска тестов подходят следующие команды:

Билд + запуск:

    $ sudo docker-compose -f docker-compose.yml -f ../../compose-redis-cluster.yml up -d --build

Только запуск:

    $ sudo docker-compose up tests

Остановка:

    $ sudo docker-compose -f docker-compose.yml -f ../../compose-redis-cluster.yml down
   
