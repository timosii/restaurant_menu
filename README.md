# Restaurant menu
# Description

Проект на FastAPI с использованием PostgreSQL в качестве БД.
В проекте реализован REST API по работе с меню ресторана, все CRUD операции.

- Реализован вывод количества подменю и блюд для меню через один ORM запрос (menu_app/repositories/menu_repository/dish_count, submenu_count;
menu_app/repositories/submenu_repository/dish_for_submenu_count)

- Реализован тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest (menu_app/tests/test_counts)

- Добавлен эндпоинт для просмотра всей структуры меню вместе с подменю и блюдами:
/api/v1/viewall


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
