# Restaurant menu
# Description

Проект на FastAPI с использованием PostgreSQL в качестве БД.
В проекте реализован REST API по работе с меню ресторана, все CRUD операции.

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
- Остановка и удаление всех контейнеров
```
make stop
```
- Удаление образов, созданных при работе программы
```
make delete-images
```
