# Restaurant menu
# Description
Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции
# Install
0. ```git clone git@github.com:timosii/restaurant_menu.git```
1. Переходим в папку с проектом
```cd restaurant_menu``` 
2. Устанавливаем пакеты
```poetry install```
3. В файл `.env` вносим свои данные для доступа к базе данных
4. Запускаем сервер
```poetry run uvicorn menu_app.main:app --reload```

