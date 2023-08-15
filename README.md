# Restaurant menu
## Technologies ##
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# Description

Проект на FastAPI с использованием PostgreSQL в качестве БД.
В проекте реализован REST API по работе с меню ресторана, все CRUD операции.
Каждое меню имеет подменю, а подменю включает в себя блюда.

- Для просмотра всей структуры меню вместе с подменю и блюдами воспользуйтесь эндпоинтом:
`/api/v1/viewall`
- Реализовано **кеширование запросов**. Инвалидация кеша проводится при помощи **background tasks**.
- Реализовано интеграционное тестирование эндпоинтов. Добавлен тестовый сценарий «Проверка кол-ва блюд и подменю в меню»:
`menu_app/tests/test_counts`
- Вывод количества подменю и блюд для меню, а также количество блюд для подменю осуществляется через один ORM запрос.
Ознакомиться с реализацией:
`menu_app/repositories/menu_repository/submenu_count`
`menu_app/repositories/menu_repository/dish_count`
`menu_app/repositories/submenu_repository/dish_for_submenu_count`
- В режиме администратора выполняется **фоновая задача** - каждые 15 секунд данные в базе данных обновляются из файла "Menu.xlsx"
- Документация доступна по адресу `/docs`
- Просмотр кеша:
  - для основной программы:
  `redis-cli -p 6380`
  - для тестов:
  `redis-cli -p 6381`


# Install

- Клонируем репозиторий
```
git clone git@github.com:timosii/restaurant_menu.git
```
- Переходим в папку с проектом
```
cd restaurant_menu
```

# Запуск в Docker

- Запуск основной программы
```
make app
```
- Запуск тестов
```
make test
```
- Запуск основной программы + запуск тестов
```
make start-all
```
- Запуск режима администратора (синхронизация с файлом Menu.xlsx в папке admin)
```
make sync-start
```
- Остановка и удаление всех контейнеров
```
make stop
```
- Удаление образов, созданных при работе программы
```
make delete-images
```
# Backlog
- [ ] Реализовать в тестах аналог Django reverse() для FastAPI
- [ ] Обновление меню из google sheets раз в 15 сек.
- [ ] Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx
